import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, jsonify
from waitress import serve
from pydub import AudioSegment
from pydub.playback import play
import time
import csv

# a function to load and process audio files in audio/ directory
def load_audio():
    print("Loading audio files...")
    
    audio = {}
    for filename in os.listdir("audio/"):
        if filename.endswith(".wav") or filename.endswith(".mp3"):
            name = filename.split(".")[0]
            audio[name] = {
                "name": name,
                "filename": f"audio/{filename}",
                "audio": AudioSegment.from_file(f"audio/{filename}")
            }

    print(f"Loaded {len(audio)} audio files")
    return audio

AUDIO = load_audio()


# instantiate the app
app = Flask(__name__)
current_log_file = (os.getenv("LOGFILE_PREFIX") or "log_") + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
print(f"New log file started: {current_log_file}")

# ping route to check if server is up
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!'), 200

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
    if name not in AUDIO or not AUDIO[name]["audio"]:
        return jsonify(message="Invalid name"), 400
    
    # create logs/ directory if it doesn't exist
    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    song = AUDIO[name]["audio"]
    try:
        print(f"Started Audio: {name}...")
        timestart = time.time_ns()
        play(song)
        print("Audio Played")

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

if __name__ == '__main__':
    PORT = os.getenv("PORT") or 5055
    print("Serving app at http://127.0.0.1:" + PORT + "/")
    serve(app, host='0.0.0.0', port=PORT)