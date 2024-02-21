from flask import Blueprint, Response, g, jsonify, request
import time
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

info_blueprint = Blueprint('info', __name__)

@info_blueprint.route('/docs', methods=['GET'])
@info_blueprint.route('/doc', methods=['GET'])
@info_blueprint.route('/documentation', methods=['GET'])
@info_blueprint.route('/documentations', methods=['GET'])
@info_blueprint.route('/help', methods=['GET'])
# also handle route with trailing slash
@info_blueprint.route('/docs/', methods=['GET'])
@info_blueprint.route('/doc/', methods=['GET'])
@info_blueprint.route('/documentation/', methods=['GET'])
@info_blueprint.route('/documentations/', methods=['GET'])
@info_blueprint.route('/help/', methods=['GET'])
def root_documentation():
    text = """
    Available routes:
        - GET /ping                         --> pong
                (eg. /ping ==> pong)


        - GET /list                         --> list all available audio files and playlists
                (eg. /list ==> Audio files: ... Playlists: ...)
                + ?json=true (optional) --> return JSON instead of plain text
						(eg. /list?json=true ==> {"audio": [...], "playlist": [...]})


        - GET /info/<name>                  --> get info about an audio file or playlist
                (eg. /info/1.wav ==> 1.wav info)
                (eg. /info/playlist_file.txt ==> playlist_file.txt info)


        - GET /reload                       --> reload the audio files and playlists from disk (the ./audio and ./playlists folders)
                (eg. /reload ==> Reloaded audio files and playlists)


        - GET /startnewlog                  --> start a new log file
                (eg. /startnewlog ==> Started new log file: ./logs/log_20210321-171234.csv)


        - GET /stop                         --> stop all playing audio
                (eg. /stop ==> Stopped all playing audio)

                
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


        - GET /playlist/<playlist_name>     --> play a playlist on the server, more verbal but have gaps between files/steps
                (eg. /playlist/playlist_file.txt ==> playlist_file.txt started playing on the server)

        
        - GET /playlist/gapless/<playlist>  --> play a playlist on the server, less verbal (similar to /play) but gapless
                (eg. /playlist/gapless/playlist_file.txt ==> playlist_file.txt started playing on the server)


        - GET /playlist/save/<playlist_name>  --> save the gapless version of the playlist as a wav file
                (eg. /playlist/save/playlist_file.txt ==> generate file "playlist_file.wav" to download)


        - GET /generate_batch_files         --> generate a .zip containing batch files to request the audio files and playlists (close when audio file is finished playing)
                (eg. /generate_batch_files ==> ZIP file to download)


        - GET /generate_batch_files_async   --> generate a .zip containing batch files to request the audio files and playlists (asynchronous, close immediately)
                (eg. /generate_batch_files_async ==> ZIP file to download)


        - GET /restart                      --> show the instructions to restart the server with HTTP request


        - GET /shutdown                     --> show instructions to shutdown the server with HTTP request
                * The server can also be shut down gracefully by pressing Ctrl+C in the terminal


                
    IMPORTANT: Audio Pre-Processing
        - In some scenarios (continue reading below), it is necessary to pre-process the audio files. The pre-processing step is done immediately when the app is booting up, right before the server is actually started (and reachable via the IP address and port number).
        
        - The audio files are pre-processed if they meet any of the following conditions:
        
            + The audio file's bit depth is higher than 16 bits. The audio server (currently) only supports 16-bit signed integer format. In this case, the audio file is simply converted to 16-bit signed integer format.

            + The audio file's sample rate is non-standard. The server can only play audio at the following sampling rates: 8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000 (Hz). In this case, the audio file is resampled to the nearest higher standard sampling rate. For example, an audio file with a sample rate of 44101 Hz will be resampled to 48000 Hz. The resampling is done using the 'resampy' library, which implements the sampling rate conversion described by: Smith, Julius O. Digital Audio Resampling Home Page Center for Computer Research in Music and Acoustics (CCRMA), Stanford University, 2015-02-23. Web published at http://ccrma.stanford.edu/~jos/resample/.

            + Only for gapless playback, all audio files in the same playlist must have the same sample rate. If the sample rates are different, the audio files are resampled to the highest sample rate in the playlist. For example, if a playlist contains audio files with sample rates of 44100 Hz and 48000 Hz, all audio files will be resampled to 48000 Hz. The resampling method is the same as described above.

            + Only for gapless playback, continue from the previous point, the same audio file might be played at different sample rates if it is in different playlists. In other words, the sample rate of different playlists can be different, all depends on the highest sample rate audio file in the playlist.

        - The pre-processed data is only stored in memory and is not saved to disk. The pre-processed data is used for playback and is discarded when the server is stopped. The original audio files are never modified.

        - Playlists are also prepared for gapless playback during the pre-processing step. The audio files in the playlist are resampled to the highest sample rate in the playlist as described above, then the resampled audio are then concatenated into a single audio file in-memory. The concatenated audio file is used for gapless playback. The concatenated audio file is only stored in memory and is not saved to disk. The original audio files are never modified.

        - It is strongly advised that the user process the audio files manually themselves if repeatability and performance are important.




    General Note:
        - All audio and playlist data are stored in memory on start up to ensure fast access. Please be mindful of the available memory (RAM) on the server.

        - Playlists can be any .txt file with a valid list of audio file names. Pauses can also be added using the `pause_{duration}ms`, for example, "pause_1000ms" for a 1-second pause. The playlist files must be in the ./playlists folder.

        - Audio file names should be limited to only the English alphabet, numbers, and typical special characters. Spaces are fine, as well.

        - For any request that would result in a log file (eg. /play, /tone, /sweep, /play/random, /playlist, etc.), an optional query string ?time=<client_time> can be added to the request to specify the client time. This is useful for estimating the client-server request delay if the client and server are synced to the same clock. Example: /play/1.wav?time=1616331234567

        - The batch files generated by /generate_batch_files and /generate_batch_files_async are for Windows only.

        - For /tone, freq is in Hz, duration is in milliseconds, amplitude is in dB, and sample_rate is in Hz.

        - /playlist playback is not truely gapless. There is a small gap between files.

        - Use /playlist/gapless for gapless playback. This will create a new log file for that session playback. The log file will contain \"playlistG\" in the file name (instead of just \"playlist\").

        - /play/random and /playlist will always create a new log file for that session playback. The log file will contain \"playrandom\" or \"playlist\" in the file name.

        - /playlist/create will also hot reload the playlists folder, so you can create a new playlist and play it right away.

        


    Start-up arguments:
        When starting the server, you can specify the following arguments:
            -h, --help: Show help message with all up-to-date available arguments. If -h is different from this documentation, then the the -h argument will take precedence.
            --no-convert-to-s16: Skip all audio files' bit depth conversion to 16-bit signed integer format and simply uses the original audio files. Note that playback is (significantly) less reliable for audio files with bit depth > 16 bits.


        Example:
            python main.py --no-convert-to-s16

            py_audio_server.exe --no-convert-to-s16

            ./py_audio_server --no-convert-to-s16




    Config File:
        You can change the port number and the log file's prefix by creating a .env file in the same directory as main.py or the executable.

        The .env file should look like this:
            PORT=5055
            LOGFILE_PREFIX="log_"

        If the .env file is not found, the default port number is 5050 and the default log file prefix is "log_".




    If Using the Executable:
        - The executable is built using PyInstaller and is a standalone file. When the executable is run, it will extract the necessary files to a temporary directory and run the server from there. The temporary directory is deleted when the server is stopped. For more information, see https://pyinstaller.org/en/stable/operating-mode.html#how-the-one-file-program-works.

        - To cleanly shut down the server, press Ctrl+C in the terminal, or use the /shutdown endpoint. Simply closing the terminal window will not shut down the server properly. If the server is not shut down properly, the temporary directory will not be deleted and take up space on the hard drive. In the worst case, you can always delete the temporary directory manually.

        - The temporary directory location is platform-dependent. On Windows, it is usually in the %TEMP% directory. On Linux, it is usually in /tmp.


    """
    return Response(text, mimetype='text/plain'), 200


@info_blueprint.route('/list', methods=['GET'])
def list_items():
	time_ns = time.time_ns()
	print(f"\n{time_ns}: Received /list")
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
    print(f"\n{time_ns}: Received /info/{name}")

    if not name:
        print(f"\x1b[2m\x1b[31m    No playlist file name provided\x1b[0m")
        return jsonify(message="No playlist file name provided"), 400

    AUDIO = g.AUDIO
    PLAYLIST = g.PLAYLIST    
    
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
        