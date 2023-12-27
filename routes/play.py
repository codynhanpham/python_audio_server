from flask import Blueprint, jsonify, g

import time, os
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

import csv
from dotenv import load_dotenv
load_dotenv()

from pydub.playback import play

import utils as utils

play_blueprint = Blueprint('play', __name__)

@play_blueprint.route('/play/<name>', methods=['GET'])
def play_audio(name):
    time_ns = time.time_ns()
    print(f"{time_ns}: Received /play/{name}")

    if not name:
        print(f"\x1b[2m\x1b[31m    No name provided\x1b[0m")
        return jsonify(message="No name provided"), 400
    
    AUDIO = g.AUDIO
    current_log_file = g.current_log_file


    
    # if AUDIO is an empty dict, return 404 error
    if not AUDIO:
        print(f"\x1b[2m\x1b[31m    No audio files found\x1b[0m")
        return jsonify(message="No audio file (.wav or .mp3) in the ./audio/ folder."), 404

    if name not in AUDIO or not AUDIO[name]["audio"]:
        print(f"\x1b[2m\x1b[31m    Audio file '{name}' not found\x1b[0m")
        return jsonify(message=f"Audio file '{name}' not found. Navigate to /list to see the available audio files and playlists."), 404
    
    # create logs/ directory if it doesn't exist
    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    song = AUDIO[name]["audio"]
    try:
        print(f"\x1b[2m\x1b[38;5;8m    Source's Sample Rate: {song.frame_rate} Hz")

        timestart = time.time_ns()
        print(f"\x1b[2m\x1b[38;5;8m    {timestart}: Started {name}...\x1b[0m")
        with utils.ignore_stderr():
            play(song)
        print(f"\x1b[2m\x1b[38;5;8m    Finished (job at {timestart})\x1b[0m")

        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([timestart, name, "success"])

        print(f"\x1b[2m\x1b[38;5;8m    Appended to log file: ./logs/{current_log_file}\x1b[0m")
        return jsonify(message=f"At {timestart}: Played {name}"), 200
    except Exception as e:
        print(f"\x1b[2m\x1b[31m    Error occurred: {e}\x1b[0m")
        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([timestart, name, "error"])
        print(f"\x1b[2m\x1b[38;5;8m    Appended (error) to log file: ./logs/{current_log_file}\x1b[0m")

        return jsonify(error=str(e), message="The server can only play audio at the following sampling rates: 8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000 (Hz). If the error is about weird sample rates, please double check your audio file."), 500