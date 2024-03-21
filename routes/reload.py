from flask import Blueprint, g, Response

import time
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

import utils as utils
import simpleaudio
import faulthandler; faulthandler.enable()

reload_blueprint = Blueprint('reload', __name__)

@reload_blueprint.route('/reload', methods=['GET'])
def reload():
    try:
        simpleaudio.stop_all()
    except:
        pass
    utils.PLAYLIST_ABORT = True
    # Reload audio files and playlists from disk
    time_ns = time.time_ns()
    print(f"\n{time_ns}: Received /reload")
    print("\x1b[2m    This will take a moment...\x1b[0m\n\n")

    # Reload audio files and playlists from disk
    CLI_ARGS = g.CLI_ARGS
    utils.AUDIO = utils.load_audio(CLI_ARGS)
    utils.PLAYLIST = utils.load_and_validate_playlists("playlists/", utils.AUDIO)

    return Response("Reloaded audio files and playlists from disk. To see the updated list, visit /list", status=200, mimetype='text/plain')