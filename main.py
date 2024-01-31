import os
import sys
def resource_path(relative_path=''):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
sys.path.append(resource_path())
os.environ["PATH"] += os.pathsep + resource_path()
sys.path.append(resource_path("bin"))
os.environ["PATH"] += os.pathsep + resource_path("bin")
_startup_cwd = os.getcwd()

BASE_PATH = resource_path()

import utils as utils

from dotenv import dotenv_values

from flask import Flask, jsonify, g
from waitress import serve

import time
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

import argparse



if __name__ == '__main__':
    config = dotenv_values(".env")
    args = sys.argv[:]
    start_command = sys.executable if args[0] == sys.executable else ' '.join([sys.executable, args[0]])

    parser = argparse.ArgumentParser(
                        prog=start_command,
                        description="API server to play audio locally from remote client's requests.")
    parser.add_argument('--no-convert-to-s16', action='store_true', help='Skip all audio files\' bit depth conversion to 16-bit signed integer format and simply uses the original audio files. Note that playback is less reliable for audio files with bit depth > 16 bits.')
    parser.add_argument('-pb','--progress-bar', action='store_true', help='Show the progress bar when playing playlists gaplessly. The progress bar is only an estimate and likely be different from what is actually playing.')

    CLI_ARGS = parser.parse_args()


    # instantiate the app
    app = Flask(__name__)



    print("\n------------------ PYTHON AUDIO SERVER ------------------")
    print("The source code for this project is available at https://github.com/codynhanpham/python_audio_server\n\n")

    IP_ADDRESS = utils.get_local_ip()
    AUDIO = utils.load_audio(CLI_ARGS=CLI_ARGS)
    utils.PLAYLIST = utils.load_and_validate_playlists("playlists/", AUDIO)

    current_log_file = config.get("LOGFILE_PREFIX", "log_") + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
    print(f"New log file started: ./logs/{current_log_file}\n")


    # Call this function before every request to share global variables
    @app.before_request
    def before_request():
        g.AUDIO = AUDIO
        g.PLAYLIST = utils.PLAYLIST
        global current_log_file
        g.current_log_file = current_log_file
        g.IP_ADDRESS = IP_ADDRESS
        g.PORT = config.get("PORT", 5055)
        g.LOGFILE_PREFIX = config.get("LOGFILE_PREFIX", "log_")
        g.BASE_PATH = BASE_PATH
        g._startup_cwd = _startup_cwd
        g.SHUTDOWN_TOKENS = utils.SHUTDOWN_TOKENS
        g.CLI_ARGS = CLI_ARGS


    # This route must be in the main file, to be able to easily change the global variable current_log_file
    @app.route('/startnewlog', methods=['GET'])
    def start_new_log():
        time_ns = time.time_ns()
        print(f"{time_ns}: Received /startnewlog")

        global current_log_file
        current_log_file = config.get("LOGFILE_PREFIX", "log_") + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
        
        print(f"New log file started: {current_log_file}")
        return jsonify(message=f"Started new log file: ./logs/{current_log_file}"), 200

    print("Preparing to serve app...\n")
    time.sleep(2.5) # in case some HTTP requests were called before the server was restarted, the delay helps timing those out.

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

    # route to /sweep/<sweep_type>/<start_freq>/<end_freq>/<duration>/<volume>/<sample_rate> (and /save_sweep) to generate a sweep and play it
    from routes.sweep import sweep_blueprint
    app.register_blueprint(sweep_blueprint)

    # route to /playlist/create and /playlist to generate a random playlist and play it
    from routes.playlist import playlist_blueprint
    app.register_blueprint(playlist_blueprint)

    # route to /batch_files to generate batch files for all audio files and playlists
    from routes.batch_files import batch_file_blueprint
    app.register_blueprint(batch_file_blueprint)

    # route to /power/_ to restart or shutdown the server
    from routes.power import power_blueprint
    app.register_blueprint(power_blueprint)


    PORT = config.get("PORT", 5055)
    print(f"Serving app at http://{IP_ADDRESS}:{PORT}/\n")
    print("(Hit Ctrl+C to quit at anytime)\n\n")
    serve(app, host='0.0.0.0', port=PORT)