from flask import Blueprint, jsonify

import time
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

import simpleaudio

stop_blueprint = Blueprint('stop', __name__)

@stop_blueprint.route('/stop', methods=['GET'])
def stop_all_audio():
    time_ns = time.time_ns()
    print(f"{time_ns}: Received /stop")
    simpleaudio.stop_all()

    print(f"\x1b[2m    Stopped all playing audio\x1b[0m")
    return jsonify(message="Stopped all playing audio"), 200

# redirect /stop/ to /stop
@stop_blueprint.route('/stop/', methods=['GET'])
def stop_all_audio_redirect():
    return stop_all_audio()