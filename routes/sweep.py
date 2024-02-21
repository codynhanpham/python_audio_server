from flask import Blueprint, jsonify, g, request, send_file, Response

import time, os
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

import io
import wave

import csv

from pydub.playback import play, _play_with_simpleaudio
import simpleaudio
import numpy as np
from scipy.signal import chirp



import utils as utils

sweep_blueprint = Blueprint('sweep', __name__)

@sweep_blueprint.route('/sweep', methods=['GET'])
@sweep_blueprint.route('/sweep/', methods=['GET'])
def sweep_docs():
    text = """
    - /sweep/<sweep_type>/<start_freq>/<end_freq>/<duration>/<volume>/<sample_rate>
        + sweep_type: "linear", "quadratic", "logarithmic", "hyperbolic"

        + start_freq: start frequency in Hz (0-200000, default = 440)

        + end_freq: end frequency in Hz (0-200000, default = 8800)

        + duration: duration in ms (default = 100)

        + volume: volume in dB (default = 60)

        + sample_rate: sample rate in Hz (default = 192000)

        + ?time= : (optional) time in ms when the request was sent (client time)

        + ?edge=-<value> (optional, default = 0) --> fade in and out the tone by <value> ms
            (value must be negative or 0, inclusive fade duration, eg. ?edge=-10)


    - /save_sweep/<sweep_type>/<start_freq>/<end_freq>/<duration>/<volume>/<sample_rate>
        (Similar to /sweep, but saves the sweep as a .wav file instead of playing it)
        

    """
    return Response(text, mimetype='text/plain')

@sweep_blueprint.route('/sweep/<sweep_type>/<start_freq>/<end_freq>/<duration>/<volume>/<sample_rate>', methods=['GET'])
def play_sweep(sweep_type, start_freq, end_freq, duration, volume, sample_rate):
    simpleaudio.stop_all()
    time_ns = time.time_ns()
    # Get the ?edge= query string, else default to nothing
    edge = request.args.get('edge') or request.args.get('edges') or 0
    print(f"\n{time_ns}: Received /sweep/{sweep_type}/{start_freq}/{end_freq}/{duration}/{volume}/{sample_rate}?edge={edge}")

    # Parse edge into an int: if float then round to nearest int
    try:
        edge = int(round(float(edge)))
        if edge > 0:
            raise ValueError
    except (TypeError, ValueError):
        print(f"\x1b[2m\x1b[31m    Edge is invalid. Must be a valid integer <= 0.\x1b[0m")
        return jsonify(error="For sweep, Edge must be a valid integer <= 0 (inclusive)."), 400
    try:
        duration = int(duration)
        if duration <= 0:
            raise ValueError
    except (TypeError, ValueError):
        print(f"\x1b[2m\x1b[31m    Duration is invalid\x1b[0m")
        return jsonify(error="Duration must be an integer > 0."), 400
    
    if edge < 0 and duration < 2*abs(edge):
        print(f"\x1b[2m\x1b[31m    Duration or edge is invalid\x1b[0m")
        return jsonify(error="For sweep, Edge must be <= 0 (inclusive), and the Duration must be greater than the absolute value of the edge times 2 (rising and falling)."), 400
    

    # create logs/ directory if it doesn't exist
    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    current_log_file = g.current_log_file

    # Get the ?time= query string, else default to nothing
    client_time = request.args.get('time') or ""

    # create the sweep
    sweep = utils.create_sweep(sweep_type, start_freq, end_freq, duration, volume, sample_rate, edge)
    edge_tag = ""
    if edge > 0:
        edge_tag = f"_+{abs(edge)}ms"
    elif edge < 0:
        edge_tag = f"_-{abs(edge)}ms"

    try:
        with utils.ignore_stderr():
            # play(sweep)
            sink = _play_with_simpleaudio(sweep)
            timestart = time.time_ns()
            print(f"\x1b[2m    {timestart}: Playing {sweep_type}_{start_freq}Hz_{end_freq}Hz_{duration}ms_{volume}dB_@{sample_rate}Hz (edge: {edge}ms)...\x1b[0m")
            sink.wait_done()
        print(f"\x1b[2m    Finished (job at {timestart})\x1b[0m")

        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([timestart, f"{sweep_type}_{start_freq}Hz_{end_freq}Hz_{duration}ms_{volume}dB_@{sample_rate}Hz{edge_tag}", "success", client_time])
        print(f"\x1b[2m    Appended to log file: ./logs/{current_log_file}\x1b[0m")

        return jsonify(message=f"At {timestart} played sweep_{sweep_type}_{start_freq}Hz_{end_freq}Hz_{duration}ms_{volume}dB_@{sample_rate}Hz{edge_tag}"), 200
    except Exception as e:
        timestart = time.time_ns()
        print(f"\x1b[2m\x1b[31m    Error occurred: {e}\x1b[0m")
        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([timestart, f"{sweep_type}_{start_freq}Hz_{end_freq}Hz_{duration}ms_{volume}dB_@{sample_rate}Hz{edge_tag}", "error", client_time])
        print(f"\x1b[2m    Appended to log file: ./logs/{current_log_file}\x1b[0m")

        return jsonify(message=f"Error occurred: {e}"), 500
    
@sweep_blueprint.route('/save_sweep/<sweep_type>/<start_freq>/<end_freq>/<duration>/<volume>/<sample_rate>', methods=['GET'])
def save_sweep(sweep_type, start_freq, end_freq, duration, volume, sample_rate):
    time_ns = time.time_ns()
    # Get the ?edge= query string, else default to nothing
    edge = request.args.get('edge') or request.args.get('edges') or 0
    print(f"\n{time_ns}: Received /save_sweep/{sweep_type}/{start_freq}/{end_freq}/{duration}/{volume}/{sample_rate}?edge={edge}")

    # validate args
    try:
        start_freq = float(start_freq)
        if start_freq < 0:
            raise ValueError
    except (TypeError, ValueError):
        start_freq = 440
        return jsonify(error="start_freq must be a number >= 0"), 400
    
    try:
        end_freq = float(end_freq)
        if end_freq < 0:
            raise ValueError
    except (TypeError, ValueError):
        end_freq = 8800
        return jsonify(error="end_freq must be a number >= 0"), 400
    
    try:
        duration = int(duration)
        if duration <= 0:
            raise ValueError
    except (TypeError, ValueError):
        duration = 100
        return jsonify(error="duration must be an integer > 0"), 400

    try:
        volume = float(volume)
    except (TypeError, ValueError):
        volume = 60
        return jsonify(error="volume must be a number"), 400
    
    try:
        sample_rate = int(sample_rate)
        if sample_rate <= 0:
            raise ValueError
    except (TypeError, ValueError):
        sample_rate = 192000
        return jsonify(error="sample_rate must be an integer > 0"), 400
    
    if sweep_type not in ["linear", "quadratic", "logarithmic", "hyperbolic"]:
        return jsonify(error="sweep_type must be one of the following: linear, quadratic, logarithmic, hyperbolic"), 400
    
    # Parse edge into an int: if float then round to nearest int
    try:
        edge = int(round(float(edge)))
        if edge > 0:
            raise ValueError
    except (TypeError, ValueError):
        print(f"\x1b[2m\x1b[31m    Edge is invalid. Must be a valid integer <= 0.\x1b[0m")
        return jsonify(error="For sweep, Edge must be a valid integer <= 0 (inclusive)."), 400
    
    if edge < 0 and duration < 2*abs(edge):
        print(f"\x1b[2m\x1b[31m    Duration or edge is invalid\x1b[0m")
        return jsonify(error="For sweep, Edge must be <= 0 (inclusive), and the Duration must be greater than the absolute value of the edge times 2 (rising and falling)."), 400

    # Create the sweep at the specified frequency and sample rate
    t = np.linspace(0, duration / 1000, duration * sample_rate // 1000)
    # Calculate the y values
    y = chirp(t, start_freq, duration / 1000, end_freq, method=sweep_type)
    # Scale the y values
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


    # Convert to 16-bit data
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
        download_name=f"{sweep_type}_{start_freq}Hz_{end_freq}Hz_{duration}ms_{volume}dB_@{sample_rate}Hz{edge_tag}.wav"
    )
