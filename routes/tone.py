from flask import Blueprint, jsonify, g

import time, os
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

import csv
from dotenv import load_dotenv
load_dotenv()

from pydub.playback import play

import utils as utils

tone_blueprint = Blueprint('tone', __name__)

@tone_blueprint.route('/tone/<frequency>/<duration>/<volume>/<sample_rate>', methods=['GET'])
def play_tone(frequency, duration, volume, sample_rate):
    time_ns = time.time_ns()
    print(f"{time_ns}: Received /tone/{frequency}/{duration}/{volume}/{sample_rate}")

    # create logs/ directory if it doesn't exist
    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    current_log_file = g.current_log_file

    # create the tone
    tone = utils.create_tone(frequency, duration, volume, sample_rate)
    try:
        timestart = time.time_ns()
        # print(f"Started Tone: {frequency} Hz, {duration} ms, {volume} dB, @ {sample_rate} Hz...")
        print(f"\x1b[2m\x1b[38;5;8m    {timestart}: Started {frequency}Hz_{duration}ms_{volume}dB_@{sample_rate}Hz...\x1b[0m")
        with utils.ignore_stderr():
            play(tone)
        print(f"\x1b[2m\x1b[38;5;8m    Finished (job at {timestart})\x1b[0m")

        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([timestart, f"{frequency}Hz_{duration}ms_{volume}dB_@{sample_rate}Hz", "success"])
        print(f"\x1b[2m\x1b[38;5;8m    Appended to log file: ./logs/{current_log_file}\x1b[0m")

        return jsonify(message=f"At {timestart} played {frequency}Hz_{duration}ms_{volume}dB_@{sample_rate}Hz"), 200
    except Exception as e:
        print(f"\x1b[2m\x1b[31m    Error occurred: {e}\x1b[0m")
        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([timestart, f"{frequency} Hz, {duration} ms, {volume} dB, @ {sample_rate} Hz", "error"])
        print(f"\x1b[2m\x1b[38;5;8m    Appended (error) to log file: ./logs/{current_log_file}\x1b[0m")

        return jsonify(error=str(e), message="The server can only play audio at the following sampling rates: 8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000 (Hz). If the error is about weird sample rates, please double check your audio file."), 500