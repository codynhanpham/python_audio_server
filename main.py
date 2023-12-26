import os
import csv
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, jsonify
from waitress import serve
from pydub.playback import play

import time
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

import utils as utils

# instantiate the app
app = Flask(__name__)


AUDIO = utils.load_audio()


current_log_file = (os.getenv("LOGFILE_PREFIX") or "log_") + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
print(f"New log file started: {current_log_file}")

# ping route to check if server is up
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(message="pong"), 200


# route to /startnewlog to start a new log file
@app.route('/startnewlog', methods=['GET'])
def start_new_log():
    global current_log_file
    current_log_file = os.getenv("LOGFILE_PREFIX") + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
    print(f"New log file started: {current_log_file}")
    return jsonify(message="New log file started"), 200


# route to /play to play audio
@app.route('/play/<name>', methods=['GET'])
def play_audio(name):
    if not name:
        return jsonify(message="No name provided"), 400
    
    # if AUDIO is an empty dict, return 404 error
    if not AUDIO:
        return jsonify(message="No audio file (.wav or .mp3) in the ./audio/ folder."), 404

    if name not in AUDIO or not AUDIO[name]["audio"]:
        return jsonify(message=f"Audio file '{name}' not found. Navigate to /list to see the available audio files and playlists."), 404
    
    # create logs/ directory if it doesn't exist
    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    song = AUDIO[name]["audio"]
    try:
        timestart = time.time_ns()
        print(f"{timestart}: Started {name}...")
        play(song)
        print(f"Finished (job at {timestart})")

        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([timestart, name, "success"])
        return jsonify(message="Audio Played Successfully"), 200
    except Exception as e:
        print(f"Error: {e}")
        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([timestart, name, "error"])
        return jsonify(message=str(e)), 500


# route to /tone/<frequency>/<duration>/<volume>/<sample_rate> to generate a tone and play it
@app.route('/tone/<frequency>/<duration>/<volume>/<sample_rate>', methods=['GET'])
def play_tone(frequency, duration, volume, sample_rate):
    # create logs/ directory if it doesn't exist
    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    # create the tone
    tone = utils.create_tone(frequency, duration, volume, sample_rate)
    try:
        print(f"Started Tone: {frequency} Hz, {duration} ms, {volume} dB, @ {sample_rate} Hz...")
        timestart = time.time_ns()
        play(tone)
        print("Tone Played")

        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([timestart, f"{frequency} Hz, {duration} ms, {volume} dB, @ {sample_rate} Hz", "success"])
        return jsonify(message="Tone Played Successfully"), 200
    except Exception as e:
        print(f"Error: {e}")
        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([timestart, f"{frequency} Hz, {duration} ms, {volume} dB, @ {sample_rate} Hz", "error"])
        return jsonify(message=str(e)), 500


if __name__ == '__main__':
    PORT = os.getenv("PORT") or 5055
    print(f"Serving app at http://127.0.0.1:{PORT}/")
    serve(app, host='0.0.0.0', port=PORT)