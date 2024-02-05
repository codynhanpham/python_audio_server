import math
from flask import Blueprint, jsonify, request, g, send_file

import time, os
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

import csv
import hashlib
import random
from functools import reduce
import numpy as np

from pydub.playback import play
from pydub import AudioSegment

from multiprocessing import Process

import utils as utils

playlist_blueprint = Blueprint('playlist', __name__)

@playlist_blueprint.route('/playlist/create', methods=['GET'])
def create_playlist():
    time_ns = time.time_ns()
    print(f"{time_ns}: Received /playlist/create")

    AUDIO = g.AUDIO
    PORT = g.PORT
    IP_ADDRESS = g.IP_ADDRESS

    if not AUDIO:
        print(f"\x1b[2m\x1b[31m    No audio files found\x1b[0m")
        return jsonify(message="No audio file (.wav or .mp3) in the ./audio/ folder."), 404

    # try to get the file_count and break_between_files from the query string, else default to 10 and 0 respectively
    try:
        file_count = int(request.args.get('file_count'))
    except (TypeError, ValueError):
        file_count = 10

    try:
        break_between_files = int(request.args.get('break_between_files'))
    except (TypeError, ValueError):
        break_between_files = 0

    try:
        no_download = request.args.get('no_download').lower() == "true"
    except AttributeError:
        no_download = False

    
    # Pick random audio files up to the file_count
    # file_count might be greater than the number of audio files, so try to pick a random file file_count times instead
    playlist = []
    total_duration = 0
    for i in range(int(file_count)):
        random_audio_file = random.choice(list(AUDIO.keys()))
        playlist.append(random_audio_file)
        total_duration += len(AUDIO[random_audio_file]["audio"])

        # Also interweave the break_between_files if it's not 0 and it's not the last file
        if break_between_files != 0 and i != int(file_count) - 1:
            playlist.append(f"pause_{break_between_files}ms")
            total_duration += break_between_files

    # Create the playlist file:
    # Literally just a text file from the playlist list
    # make sure the playlist folder exists
    if not os.path.exists("playlists/"):
        os.makedirs("playlists/")

    playlist_file_name = f"playlist_{hashlib.sha256(str(playlist).encode()).hexdigest()[:8]}_{total_duration/1000}s_{len(playlist)}count.txt"
    playlist_file = open(f"playlists/{playlist_file_name}", "w")
    playlist_file.write("\n".join(playlist))
    playlist_file.close()


    # Also hot reload the playlists folder
    print(" !! Hot Reloading Playlists !!")
    utils.PLAYLIST = utils.load_and_validate_playlists("playlists/", AUDIO)


    # If no_download is true, return the playlist name
    if no_download:
        return jsonify(message=f"Created new playlist file server-side: ./playlists/{playlist_file_name}. To play this new playlist, visit http://{IP_ADDRESS}:{PORT}/playlist/{playlist_file_name}", filename=playlist_file_name), 200
    
    # Else, return the playlist file for download
    return send_file(f"playlists/{playlist_file_name}", as_attachment=True), 200


@playlist_blueprint.route('/playlist/<name>', methods=['GET'])
def play_playlist(name):
    time_ns = time.time_ns()
    print(f"{time_ns}: Received /playlist/{name}")

    if not name:
        print(f"\x1b[2m\x1b[31m    No playlist file name provided\x1b[0m")
        return jsonify(message="No playlist file name provided"), 400
    
    AUDIO = g.AUDIO
    PLAYLIST = g.PLAYLIST
    logfile_prefix = g.LOGFILE_PREFIX

    # if AUDIO is an empty dict, return 404 error
    if not AUDIO:
        print(f"\x1b[2m\x1b[31m    No audio files found\x1b[0m")
        return jsonify(message="No audio file (.wav or .mp3) in the ./audio/ folder."), 404

    if name not in PLAYLIST:
        print(f"\x1b[2m\x1b[31m    Playlist file '{name}' not found\x1b[0m")
        return jsonify(message=f"Playlist file '{name}' not found. Navigate to /list to see the available audio files and playlists."), 404

    # the log file for playlist is separate from the main log file, and is specific to the playlist session
    # the prefix will be the LOGFILE_PREFIX env variable (or log) + "playlist_" + the current time
    current_log_file = logfile_prefix + "playlist_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

    playlist = PLAYLIST[name]["data"]

    # if the playlist is empty, return 404 error
    if not playlist:
        print(f"\x1b[2m\x1b[31m    Playlist '{name}' is empty\x1b[0m")
        return jsonify(message=f"Playlist '{name}' is empty."), 404
    
    # make sure the logs/ directory exists, also create the log file
    if not os.path.exists("logs/"):
        os.makedirs("logs/")
    with open("logs/" + current_log_file, 'w', newline='') as csvfile:
        logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        logwriter.writerow(["timestamp_audio", "audio_filename", "status", "timestamp_client"])

    # The first row of the log file is the request name and timestamp + client timestamp if it exists
    # Get the ?time= query string, else default to nothing
    client_time = request.args.get('time') or ""
    with open("logs/" + current_log_file, 'a', newline='') as csvfile:
        logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        logwriter.writerow([time.time_ns(), f"Received /playlist/{name}", "success", client_time])
    print(f"\x1b[2m    Appended request info to log file: ./logs/{current_log_file}\x1b[0m")

    log_data = ""
    try:
        time_ns_playback = time.time_ns()
        count = 0
        # Playlist format is a Vec of {type: "audio" or "pause", value: "filename" or "pause_duration in ms"}
        # Iterate through the playlist and play each file: Either play the audio file, or Sleep for the duration
        for step in playlist:
            if step["type"] == "audio":
                audiofile = AUDIO[step["value"]]
                source = audiofile["audio"]

                timestart = time.time_ns()
                print(f"\x1b[32m    [{count+1}/{len(playlist)}] {timestart}: Playing {step['value']}...\x1b[0m")
                with utils.ignore_stderr():
                    play(source)
                print(f"\x1b[2m    Finished (job at {timestart})\x1b[0m")

                # write to log file
                # with open("logs/" + current_log_file, 'a', newline='') as csvfile:
                #     logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                #     logwriter.writerow([timestart, step["value"], "success", "N/A"])
                # print(f"\x1b[2m    Appended to log file: ./logs/{current_log_file}\x1b[0m")
                log_data += f"{timestart},{step['value']},success,N/A\n"

                count += 1

            elif step["type"] == "pause":
                timestart = time.time_ns()
                print(f"\x1b[34m    [{count+1}/{len(playlist)}] {timestart}: Pausing for {step['value']}ms...\x1b[0m")
                time.sleep(step["value"]/1000)

                # write to log file
                # with open("logs/" + current_log_file, 'a', newline='') as csvfile:
                #     logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                #     logwriter.writerow([timestart, f"pause_{step['value']}ms", "success", "N/A"])
                # print(f"\x1b[2m    Appended to log file: ./logs/{current_log_file}\x1b[0m")
                log_data += f"{timestart},pause_{step['value']}ms,success,N/A\n"

                count += 1

        # write to log file the playback data
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            csvfile.write(log_data)
        print(f"\x1b[2m    Appended to log file: ./logs/{current_log_file}\x1b[0m")

        playback_duration = (time.time_ns() - time_ns_playback)/1_000_000_000
        request_duration = (time.time_ns() - time_ns)/1_000_000_000
        print(f"    --> At {time_ns_playback} started playlist {name} ({len(playlist)} audio files / steps). Playback took {playback_duration} seconds. Total time since request: {request_duration} seconds.\n\n")

        return jsonify(message=f"At {time_ns_playback} started playlist {name} ({len(playlist)} audio files / steps). Playback took {playback_duration} seconds. Total time since request: {request_duration} seconds."), 200
    except Exception as e:
        print(f"\x1b[2m\x1b[31m    Error occurred: {e}\x1b[0m")
        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # add whatever log data was written before the error
            if log_data:
                csvfile.write(log_data)
            logwriter.writerow([time.time_ns(), name, "playlist playback error", "N/A"])
        print(f"\x1b[2m    Appended (error) to log file: ./logs/{current_log_file}\x1b[0m")

        return jsonify(error=str(e), message="The server can only play audio at the following sampling rates: 8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000 (Hz). If the error is about weird sample rates, please double check your audio file."), 500


@playlist_blueprint.route('/playlist/gapless/<name>', methods=['GET'])
def play_playlist_gapless(name):
    time_ns = time.time_ns()
    print(f"{time_ns}: Received /playlist/gapless/{name}")

    if not name:
        print(f"\x1b[2m\x1b[31m    No playlist file name provided\x1b[0m")
        return jsonify(message="No playlist file name provided"), 400
    
    AUDIO = g.AUDIO
    PLAYLIST = g.PLAYLIST
    logfile_prefix = g.LOGFILE_PREFIX

    # if AUDIO is an empty dict, return 404 error
    if not AUDIO:
        print(f"\x1b[2m\x1b[31m    No audio files found\x1b[0m")
        return jsonify(message="No audio file (.wav or .mp3) in the ./audio/ folder."), 404

    if name not in PLAYLIST:
        print(f"\x1b[2m\x1b[31m    Playlist file '{name}' not found\x1b[0m")
        return jsonify(message=f"Playlist file '{name}' not found. Navigate to /list to see the available audio files and playlists."), 404

    # the log file for playlist is separate from the main log file, and is specific to the playlist session
    # the prefix will be the LOGFILE_PREFIX env variable (or log) + "playlist_" + the current time
    current_log_file = logfile_prefix + "playlistG_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

    playlist = PLAYLIST[name]["data"]

    # if the playlist is empty, return 404 error
    if not playlist:
        print(f"\x1b[2m\x1b[31m    Playlist '{name}' is empty\x1b[0m")
        return jsonify(message=f"Playlist '{name}' is empty."), 404
    
    # make sure the logs/ directory exists, also create the log file
    if not os.path.exists("logs/"):
        os.makedirs("logs/")
    with open("logs/" + current_log_file, 'w', newline='') as csvfile:
        logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        logwriter.writerow(["timestamp_audio", "audio_filename", "status", "timestamp_client"])

    # The first row of the log file is the request name and timestamp + client timestamp if it exists
    # Get the ?time= query string, else default to nothing
    client_time = request.args.get('time') or ""
    with open("logs/" + current_log_file, 'a', newline='') as csvfile:
        logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        logwriter.writerow([time.time_ns(), f"Received /playlist/gapless/{name}", "success", client_time])
    print(f"\x1b[2m    Appended request info to log file: ./logs/{current_log_file}\x1b[0m")

    highest_samplerate = max((AUDIO[step["value"]]["audio"].frame_rate for step in playlist if step["type"] == "audio"), default=48000)

    # For gapless, create a single audio segment from all the audio files in the playlist first
    # Since it is gapless, no need to add log for each audio file
    # For pause, create a single audio segment of silence for the duration
    # Then play the single audio segment
    process = None
    try:
        print(f"\x1b[34m    Note: For this playlist gapless playback, all audio files will be resampled to {highest_samplerate} Hz\x1b[0m")

        playlistSegment = AudioSegment.empty()
        chapters = []
        total_array_length = 0

        # try to use numpy for concatenation (simply appending AudioSegments is too slow as the AudioSegments are immutable)
        # also, have to make sure all audio files are of the same sample rate, sample width, and channels
        # (forces resampling to highest_samplerate Hz, 2 channels, 16-bit sample width)
        nparrays = []
        for step in playlist:
            if step["type"] == "audio":
                audiofile = AUDIO[step["value"]]
                source = audiofile["audio"]

                if source.frame_rate != highest_samplerate:
                    source = utils.resample_audio(source, highest_samplerate)

                if source.channels != 2:
                    source = source.set_channels(2)

                if source.sample_width != 2:
                    source = source.set_sample_width(2)

                # convert source to numpy array
                nparray = source.get_array_of_samples()
                total_array_length += len(nparray)

                # append the numpy array to the list of numpy arrays
                if nparray is not None:
                    nparrays.append(nparray)

                # chapter with [end_time, name]
                chapters.append([total_array_length / (highest_samplerate * 2) * 1000, step["value"]])

            elif step["type"] == "pause":
                silence =  utils.create_tone(0, step["value"], 0, highest_samplerate, 0, 2)
                nparray = silence.get_array_of_samples()
                total_array_length += len(nparray)

                # append the numpy array to the list of numpy arrays
                if nparray is not None:
                    nparrays.append(nparray)

                chapters.append([total_array_length / (highest_samplerate * 2) * 1000, f"pause_{step['value']}ms"])

        # concatenate all numpy arrays in the list
        fullnparray = np.concatenate(nparrays)

        # convert the collective numpy array to AudioSegment
        playlistSegment = AudioSegment(fullnparray.tobytes(), frame_rate=highest_samplerate, sample_width=2, channels=2)


        if g.CLI_ARGS.progress_bar:
            time_start_process = time.time_ns() // 1_000_000
            # start a progress timer in a separate process
            process = Process(target=utils.playlist_progress_timer, args=(len(playlistSegment), chapters, "", 50, time_start_process))
            process.start()

        time_ns_playback = time.time_ns()
        print(f"\x1b[32m    {time_ns_playback}: Playing {name}...\x1b[0m")
        with utils.ignore_stderr():
            play(playlistSegment)
            time_ns_end = time.time_ns()
        # terminate the progress timer
        if g.CLI_ARGS.progress_bar and process and process.is_alive():
            process.terminate()
        print(f"\x1b[2m    Finished playing {name} (job at {time_ns_playback})\x1b[0m")


        # write to log file the playback duration
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([time_ns_playback, f"Started {name}", "success", "N/A"])
            logwriter.writerow([time_ns_end, f"Finished {name} | playback took {round(((time_ns_end - time_ns_playback)/1000000), 2)} ms", "success", "N/A"])

        playback_duration = (time_ns_end - time_ns_playback)/1_000_000_000
        request_duration = (time_ns_end - time_ns)/1_000_000_000

        print(f"    --> At {time_ns_playback} started (gapless) playlist {name} ({len(playlist)} audio files / steps). Playback took {playback_duration} seconds. Total time since request: {request_duration} seconds.\n\n")

        return jsonify(message=f"At {time_ns_playback} started (gapless) playlist {name} ({len(playlist)} audio files / steps). Playback took {playback_duration} seconds. Total time since request: {request_duration} seconds."), 200
    
    except Exception as e:
        if process and process.is_alive():
            process.terminate()
        print(f"\x1b[2m\x1b[31m    Error occurred: {e}\x1b[0m")
        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([time.time_ns(), name, "playlist playback error", "N/A"])
        print(f"\x1b[2m    Appended (error) to log file: ./logs/{current_log_file}\x1b[0m")

        return jsonify(error=str(e), message="The server can only play audio at the following sampling rates: 8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000 (Hz). If the error is about weird sample rates, please double check your audio file."), 500