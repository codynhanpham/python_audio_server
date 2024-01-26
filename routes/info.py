from flask import Blueprint, Response, g, jsonify, request
import time
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

info_blueprint = Blueprint('info', __name__)

@info_blueprint.route('/', methods=['GET'])
def root_documentation():
    text = """
    Available routes:
        - GET /ping                         --> pong
                (eg. /ping ==> pong)


        - GET /list                         --> list all available audio files and playlists
                (eg. /list ==> Audio files: ... Playlists: ...)
                + ?json=true (optional) --> return JSON instead of plain text
						(eg. /list?json=true ==> {"audio": [...], "playlist": [...]})


        - GET /startnewlog                  --> start a new log file
                (eg. /startnewlog ==> Started new log file: ./logs/log_20210321-171234.csv)

                
        - GET /play/<audio_file_name>       --> play the audio file
                (eg. /play/1.wav ==> 1.wav started playing on the server)


        - GET /tone/<freq>/<duration>/<amplitude>/<sample_rate> 
                                            --> play a pure sine tone
                (eg. /tone/1000/500/40/96000 ==> 1000Hz tone started playing on the server for 500ms at 40dB)
                + ?edge=<value> (optional, default = 0) --> fade in and out the tone by <value> ms
                        (inclusive fade duration if <value> is negative, additive fade duration if <value> is positive)


        - GET /save_tone/<freq>/<duration>/<amplitude>/<sample_rate>
                                            --> create a .wav file of a pure sine tone
                (eg. /save_tone/1000/500/40/96000 ==> generate file "1000.0Hz_500ms_40.0dB_@96000Hz.wav" to download)
                + ?edge=<value> (optional, default = 0) --> fade in and out the tone by <value> ms
                        (inclusive fade duration if <value> is negative, additive fade duration if <value> is positive)


        - GET /sweep/<sweep_type>/<start_freq>/<end_freq>/<duration>/<volume>/<sample_rate>
                                            --> play a sweep
                (eg. /sweep/linear/1000/10000/500/40/96000 ==> linear sweep from 1000Hz to 10000Hz in 500ms started playing on the server at 40dB)
                + sweep_type: "linear", "quadratic", "logarithmic", "hyperbolic"

                + ?edge=-<value> (optional, default = 0) --> fade in and out the tone by <value> ms
                        (value must be negative, inclusive fade duration, eg. ?edge=-10)


        - GET /save_sweep/<sweep_type>/<start_freq>/<end_freq>/<duration>/<volume>/<sample_rate>
                                            --> create a .wav file of a sweep
                (eg. /save_sweep/linear/1000/10000/500/40/96000 ==> generate file "linear_1000.0Hz_10000.0Hz_500ms_40.0dB_@96000Hz.wav)
                + sweep_type: "linear", "quadratic", "logarithmic", "hyperbolic"

                + ?edge=-<value> (optional, default = 0) --> fade in and out the tone by <value> ms
                        (value must be negative, inclusive fade duration, eg. ?edge=-10)


        - GET /play/random                  --> play some random audio files. 2 optional parameters:
                - break_between_files (in milliseconds, default = 0)
                - file_count (number of files to play, default = 100)
                (eg. /play/random?break_between_files=1000&file_count=10 ==> 10 random files started playing on the server)


        - GET /playlist/create              --> create a random playlist with available audio files. 3 optional parameters:
                - break_between_files (in milliseconds, default = 0)
                - file_count (number of files to play, default = 100)
                - no_download (don't download the files, only create the playlist server-side and return the new playlist name, default = false)
                (eg. /playlist/create?break_between_files=1000&file_count=10 ==> random playlist: playlist_<hash>_<duration>s_<size>count.txt to download)
                (eg. /playlist/create?break_between_files=1000&file_count=20&no_download=true ==> random playlist: playlist_<hash>_<duration>s_<size>count.txt created on the server)
                
                * The <hash> is the first 8 characters of the SHA256 hash of the playlist file. This serves as a unique identifier for the playlist, so that no two duplicate playlists are created.


        - GET /playlist/<playlist_name>     --> play a playlist on the server
                (eg. /playlist/playlist_file.txt ==> playlist_file.txt started playing on the server)


        - GET /generate_batch_files         --> generate a .zip containing batch files to request the audio files and playlists (close when audio file is finished playing)
                (eg. /generate_batch_files ==> ZIP file to download)


        - GET /generate_batch_files_async   --> generate a .zip containing batch files to request the audio files and playlists (asynchronous, close immediately)
                (eg. /generate_batch_files_async ==> ZIP file to download)
        


    Note:
        - For any request that would result in a log file (eg. /play, /tone, /sweep, /play/random, /playlist, etc.), an optional query string ?time=<client_time> can be added to the request to specify the client time. This is useful for estimating the client-server request delay if the client and server are synced to the same clock. Example: /play/1.wav?time=1616331234567

        - The batch files generated by /generate_batch_files and /generate_batch_files_async are for Windows only.

        - For /tone, freq is in Hz, duration is in milliseconds, amplitude is in dB, and sample_rate is in Hz.

        - /playlist playback is not truely gapless. There is a small gap between files.

        - /play/random and /playlist will always create a new log file for that session playback. The log file will contain \"playrandom\" or \"playlist\" in the file name.

        - /playlist/create will also hot reload the playlists folder, so you can create a new playlist and play it right away.

    """
    return Response(text, mimetype='text/plain'), 200


@info_blueprint.route('/list', methods=['GET'])
def list_items():
	time_ns = time.time_ns()
	print(f"{time_ns}: Received /list")
	AUDIO = g.AUDIO
	audio_names = sorted(AUDIO.keys())

	PLAYLIST = g.PLAYLIST
	playlist_names = sorted(PLAYLIST.keys())

	text = f"""
	Audio files ({len(AUDIO)}):\n\n        {chr(9)}{f"{chr(10)}        {chr(9)}".join(audio_names)}\n\n\n

	Playlists ({len(PLAYLIST)}):\n\n        {chr(9)}{f"{chr(10)}        {chr(9)}".join(playlist_names)}\n\n\n
	"""

	# Get the ?json= query string, else default to nothing
	withjson = request.args.get('json') or ""
	if withjson == "true":
		return jsonify(audio=audio_names, playlist=playlist_names), 200

	return Response(text, mimetype='text/plain'), 200

@info_blueprint.route('/info', methods=['GET'])
def info_note():
    text = """
        To get info about an audio file or playlist, use /info/<name>
                (eg. /info/1.wav ==> 1.wav info)
                (eg. /info/playlist_file.txt ==> playlist_file.txt info)

    """
    return Response(text, mimetype='text/plain'), 200



@info_blueprint.route('/info/<name>', methods=['GET'])
def item_info(name):
    time_ns = time.time_ns()
    print(f"{time_ns}: Received /playlist/{name}")

    if not name:
        print(f"\x1b[2m\x1b[31m    No playlist file name provided\x1b[0m")
        return jsonify(message="No playlist file name provided"), 400

    AUDIO = g.AUDIO
    PLAYLIST = g.PLAYLIST

    # if AUDIO is an empty dict, return 404 error
    if not AUDIO:
        print(f"\x1b[2m\x1b[31m    No audio files found\x1b[0m")
        return jsonify(message="No audio file (.wav or .mp3) in the ./audio/ folder."), 404
    
    # if PLAYLIST is an empty dict, return 404 error
    if not PLAYLIST:
        print(f"\x1b[2m\x1b[31m    No playlist files found\x1b[0m")
        return jsonify(message="No playlist file (.txt) in the ./playlists/ folder."), 404
    
    
    # check if name is an audio file or playlist or neither
    if name in AUDIO:
        type = "audio"
    elif name in PLAYLIST:
        type = "playlist"
    else:
        print(f"\x1b[2m\x1b[31m    {name} not found\x1b[0m")
        return jsonify(message=f"{name} does not exists in ./audio or ./playlists ; or it is invalid."), 404
    

    # if name is an audio file, return the audio file info
    if type == "audio":
        info = AUDIO[name]["info"]

        # Return audio file info as plain text
        return Response(info, mimetype='text/plain'), 200
    
    # if name is a playlist, return the playlist info
    elif type == "playlist":
        info = PLAYLIST[name]["info"]

        # Return playlist info as plain text
        return Response(info, mimetype='text/plain'), 200
    
    # Should not reach here, but handle it anyway
    else:
        print(f"\x1b[2m\x1b[31m    {name} not found\x1b[0m")
        return jsonify(message=f"{name} does not exists in ./audio or ./playlists ; or it is invalid."), 404
        