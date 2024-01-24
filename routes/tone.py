from flask import Blueprint, jsonify, g, request, send_file

import time, os
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

import io
import wave

import csv

from pydub.playback import play
import numpy as np


import utils as utils

tone_blueprint = Blueprint('tone', __name__)

@tone_blueprint.route('/tone/<frequency>/<duration>/<volume>/<sample_rate>', methods=['GET'])
def play_tone(frequency, duration, volume, sample_rate):
    time_ns = time.time_ns()
    # Get the ?edge= query string, else default to nothing
    edge = request.args.get('edge') or request.args.get('edges') or 0
    print(f"{time_ns}: Received /tone/{frequency}/{duration}/{volume}/{sample_rate}?edge={edge}")

    # Parse edge into an int: if float then round to nearest int
    try:
        edge = int(round(float(edge)))
    except (TypeError, ValueError):
        print(f"\x1b[2m\x1b[31m    Edge is invalid. Must be a valid integer.\x1b[0m")
        return jsonify(error="Edge must be a valid integer, positive or negative."), 400
    try:
        duration = int(duration)
        if duration <= 0:
            raise ValueError
    except (TypeError, ValueError):
        print(f"\x1b[2m\x1b[31m    Duration is invalid\x1b[0m")
        return jsonify(error="Duration must be an integer > 0."), 400
    
    if edge < 0 and duration < 2*abs(edge):
        print(f"\x1b[2m\x1b[31m    Duration or edge is invalid\x1b[0m")
        return jsonify(error="If Edge < 0 (inclusive), the Duration must be greater than the absolute value of the edge times 2 (rising and falling). Did you mean to use a positive Edge value to add the edge duration to the tone?"), 400

    # create logs/ directory if it doesn't exist
    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    current_log_file = g.current_log_file

    # Get the ?time= query string, else default to nothing
    client_time = request.args.get('time') or ""

    # create the tone
    tone = utils.create_tone(frequency, duration, volume, sample_rate, edge)
    edge_tag = ""
    if edge > 0:
        edge_tag = f"_+{abs(edge)}ms"
    elif edge < 0:
        edge_tag = f"_-{abs(edge)}ms"

    try:
        timestart = time.time_ns()
        print(f"\x1b[2m    {timestart}: Playing {frequency}Hz_{duration}ms_{volume}dB_@{sample_rate}Hz (edge: {edge}ms)...\x1b[0m")
        with utils.ignore_stderr():
            play(tone)
        print(f"\x1b[2m    Finished (job at {timestart})\x1b[0m")

        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([timestart, f"{frequency}Hz_{duration}ms_{volume}dB_@{sample_rate}Hz{edge_tag}", "success", client_time])
        print(f"\x1b[2m    Appended to log file: ./logs/{current_log_file}\x1b[0m")

        return jsonify(message=f"At {timestart} played {frequency}Hz_{duration}ms_{volume}dB_@{sample_rate}Hz{edge_tag}"), 200
    except Exception as e:
        print(f"\x1b[2m\x1b[31m    Error occurred: {e}\x1b[0m")
        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([timestart, f"{frequency}Hz_{duration}ms_{volume}dB_@{sample_rate}Hz{edge_tag}", "error", client_time])
        print(f"\x1b[2m    Appended (error) to log file: ./logs/{current_log_file}\x1b[0m")

        return jsonify(error=str(e), message="The server can only play audio reliably at the following sampling rates: 8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000 (Hz). If the error is about weird sample rates, please double check your audio file."), 500
    

@tone_blueprint.route('/save_tone/<frequency>/<duration>/<volume>/<sample_rate>', methods=['GET'])
def save_tone(frequency, duration, volume, sample_rate):
    time_ns = time.time_ns()
    # Get the ?edge= query string, else default to nothing
    edge = request.args.get('edge') or request.args.get('edges') or 0
    print(f"{time_ns}: Received /save_tone/{frequency}/{duration}/{volume}/{sample_rate}?edge={edge}")

    # validate the arguments: frequency and volume must be numbers, duration and sample_rate must be integers
    try:
        frequency = float(frequency)

        # only >=0 though
        if frequency < 0:
            raise ValueError
    except (TypeError, ValueError):
        print(f"\x1b[2m\x1b[31m    Frequency is invalid\x1b[0m")
        return jsonify(error="Frequency must be a number larger or equal to 0."), 400
    
    try:
        duration = int(duration)
        if duration <= 0:
            raise ValueError
    except (TypeError, ValueError):
        print(f"\x1b[2m\x1b[31m    Duration is invalid\x1b[0m")
        return jsonify(error="Duration must be an integer > 0."), 400
    
    try:
        volume = float(volume)
    except (TypeError, ValueError):
        print(f"\x1b[2m\x1b[31m    Volume is invalid\x1b[0m")
        return jsonify(error="Volume must be a number."), 400
    
    try:
        sample_rate = int(sample_rate)
        if sample_rate <= 0:
            raise ValueError
    except (TypeError, ValueError):
        print(f"\x1b[2m\x1b[31m    Sample rate is invalid\x1b[0m")
        return jsonify(error="Sample rate must be an integer > 0."), 400
    
    # Parse edge into an int: if float then round to nearest int
    try:
        edge = int(round(float(edge)))
    except (TypeError, ValueError):
        print(f"\x1b[2m\x1b[31m    Edge is invalid. Must be a valid integer.\x1b[0m")
        return jsonify(error="Edge must be a valid integer, positive or negative."), 400
    
    if edge < 0 and duration < 2*abs(edge):
        print(f"\x1b[2m\x1b[31m    Duration or edge is invalid\x1b[0m")
        return jsonify(error="If Edge < 0 (inclusive), the Duration must be greater than the absolute value of the edge times 2 (rising and falling). Did you mean to use a positive Edge value to add the edge duration to the tone?"), 400

    # modify the total duration if edge is specified:
    # edge < 0: the ramp duration is already included in the duration --> no modification
    # edge > 0: the ramp duration is not included in the duration --> add the ramp duration (2 * edge) to the duration
    original_duration = duration # save this for the filename
    if edge > 0:
        duration += 2 * edge

    # create the tone and return as a wav file for download
    # calculate the number of samples
    samples = int(sample_rate * duration / 1000)
    # calculate the x values
    x = np.arange(samples)
    # calculate the y values
    y = np.sin(2 * np.pi * frequency * x / sample_rate)
    # scale the y values
    y *= 10 ** (volume / 20)

    if edge != 0:
        # calculate the number of edge samples
        edge_samples = int(sample_rate * abs(edge) / 1000)

        # create the fade-in and fade-out ramps
        fade_in = np.linspace(0, 1, edge_samples)
        fade_out = fade_in[::-1]

        # apply the fade-in and fade-out
        y[:edge_samples] *= fade_in
        y[-edge_samples:] *= fade_out

    # convert to 16-bit data
    y = y.astype(np.int16)

    output = io.BytesIO()
    # create a wave file in memory
    with wave.open(output, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)  # 16-bit samples
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(y.tobytes())

    wav_data = output.getvalue()

    edge_tag = ""
    if edge > 0:
        edge_tag = f"_+{abs(edge)}ms"
    elif edge < 0:
        edge_tag = f"_-{abs(edge)}ms"

    return send_file(
        io.BytesIO(wav_data),
        mimetype='audio/wav',
        as_attachment=True,
        attachment_filename=f"{frequency}Hz_{original_duration}ms_{volume}dB_@{sample_rate}Hz{edge_tag}.wav"
    )
