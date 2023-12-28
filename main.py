import os
import sys
# need to add path to resource (pyinstaller) for ffmpeg and ffprobe
sys.path.append(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))))
os.environ["PATH"] += os.pathsep + getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

import utils as utils

from dotenv import dotenv_values
config = dotenv_values(".env")
from flask import Flask, jsonify, g
from waitress import serve

import time
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)


# instantiate the app
app = Flask(__name__)

print("\n------------------ PYTHON AUDIO SERVER ------------------")
print("The source code for this project is available at https://github.com/codynhanpham/python_audio_server\n\n")

IP_ADDRESS = utils.get_local_ip()
AUDIO = utils.load_audio()
utils.PLAYLIST = utils.load_and_validate_playlists("playlists/", AUDIO)

current_log_file = (config["LOGFILE_PREFIX"] or "log_") + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
print(f"New log file started: ./logs/{current_log_file}\n")


# Call this function before every request to share global variables
@app.before_request
def before_request():
    g.AUDIO = AUDIO
    g.PLAYLIST = utils.PLAYLIST
    global current_log_file
    g.current_log_file = current_log_file
    g.IP_ADDRESS = IP_ADDRESS
    g.PORT = config["PORT"] or 5055
    g.LOGFILE_PREFIX = config["LOGFILE_PREFIX"] or "log_"


# This route must be in the main file, to be able to easily change the global variable current_log_file
@app.route('/startnewlog', methods=['GET'])
def start_new_log():
    time_ns = time.time_ns()
    print(f"{time_ns}: Received /startnewlog")

    global current_log_file
    current_log_file = (config["LOGFILE_PREFIX"] or "log_") + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
    
    print(f"New log file started: {current_log_file}")
    return jsonify(message=f"Started new log file: ./logs/{current_log_file}"), 200


# ping route to check if server is up
from routes.ping import ping_blueprint
app.register_blueprint(ping_blueprint)

# info/documentation at /, and list of audio files and playlists at /list
from routes.info import info_blueprint
app.register_blueprint(info_blueprint)

# route to /play and /play/random to play audio
from routes.play import play_blueprint
app.register_blueprint(play_blueprint)

# route to /tone/<frequency>/<duration>/<volume>/<sample_rate> (and /save_tone) to generate a tone and play it
from routes.tone import tone_blueprint
app.register_blueprint(tone_blueprint)

# route to /playlist/create and /playlist to generate a random playlist and play it
from routes.playlist import playlist_blueprint
app.register_blueprint(playlist_blueprint)


if __name__ == '__main__':
    PORT = config["PORT"] or 5055
    print(f"Serving app at http://{IP_ADDRESS}:{PORT}/\n")
    print("(Hit Ctrl+C to quit at anytime)\n\n")
    serve(app, host='0.0.0.0', port=PORT)