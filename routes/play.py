from flask import Blueprint, jsonify, g, request

import time, os
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

import csv
import random

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
    
    # Get the ?time= query string, else default to nothing
    client_time = request.args.get('time') or ""

    # create logs/ directory if it doesn't exist
    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    source = AUDIO[name]["audio"]
    try:
        print(f"\x1b[2m    Source's Sample Rate: {source.frame_rate} Hz")

        timestart = time.time_ns()
        print(f"\x1b[2m    {timestart}: Playing {name}...\x1b[0m")
        with utils.ignore_stderr():
            play(source)
        print(f"\x1b[2m    Finished (job at {timestart})\x1b[0m")

        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([timestart, name, "success", client_time])

        print(f"\x1b[2m    Appended to log file: ./logs/{current_log_file}\x1b[0m")
        return jsonify(message=f"At {timestart}: Played {name}"), 200
    except Exception as e:
        print(f"\x1b[2m\x1b[31m    Error occurred: {e}\x1b[0m")
        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([timestart, name, "error", client_time])
        print(f"\x1b[2m    Appended (error) to log file: ./logs/{current_log_file}\x1b[0m")

        return jsonify(error=str(e), message="The server can only play audio reliably at the following sampling rates: 8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000 (Hz). If the error is about weird sample rates, please double check your audio file."), 500
    

@play_blueprint.route('/play/random', methods=['GET'])
def play_random():
    time_ns = time.time_ns()
    print(f"{time_ns}: Received /play/random")

    AUDIO = g.AUDIO
    current_log_file = g.current_log_file
    logfile_prefix = g.LOGFILE_PREFIX

    # if AUDIO is an empty dict, return 404 error
    if not AUDIO:
        print(f"\x1b[2m\x1b[31m    No audio files found\x1b[0m")
        return jsonify(message="No audio file (.wav or .mp3) in the ./audio/ folder."), 404

    # Get the ?time= query string, else default to nothing
    client_time = request.args.get('time') or ""

    # Parse the queries: file_count, break_between_files, both must be integers
    try:
        file_count = int(request.args.get('file_count'))
    except (TypeError, ValueError):
        file_count = 100

    try:
        break_between_files = int(request.args.get('break_between_files'))
    except (TypeError, ValueError):
        break_between_files = 0


    # the log file for playlist is separate from the main log file, and is specific to the playlist session
    # the prefix will be the LOGFILE_PREFIX env variable (or log) + "playlist_" + the current time        
    current_log_file = logfile_prefix + "playrandom_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

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
        logwriter.writerow([time.time_ns(), f"Received /play/random (break: {break_between_files} ms | file_count: {file_count})", "success", client_time])
    print(f"\x1b[2m    Appended request info to log file: ./logs/{current_log_file}\x1b[0m")

    try:
        time_ns_playback = time.time_ns()
        count = 0
        while count < file_count:
            # choose a random audio file
            name = random.choice(list(AUDIO.keys()))
            source = AUDIO[name]["audio"]

            timestart = time.time_ns()
            print(f"\x1b[32m    [{count + 1}/{file_count}] {timestart}: Playing {name}...\x1b[0m")
            with utils.ignore_stderr():
                play(source)
            print(f"\x1b[2m    Finished (job at {timestart})\x1b[0m")

            # write to log file
            with open("logs/" + current_log_file, 'a', newline='') as csvfile:
                logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                logwriter.writerow([timestart, name, "success", "N/A"])

            print(f"\x1b[2m    Appended to log file: ./logs/{current_log_file}\x1b[0m")

            if break_between_files > 0 and count < file_count - 1:
                timestart = time.time_ns()
                print(f"\x1b[34m    Pausing for {break_between_files} ms...\x1b[0m")
                time.sleep(break_between_files / 1000)

                # write to log file
                with open("logs/" + current_log_file, 'a', newline='') as csvfile:
                    logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    logwriter.writerow([timestart, f"pause_{break_between_files}ms", "success", "N/A"])
                print(f"\x1b[2m    Appended (pause/break/interval) to log file: ./logs/{current_log_file}\x1b[0m")

            count += 1

        playback_duration = (time.time_ns() - time_ns_playback) / 1e9
        request_duration = (time.time_ns() - time_ns) / 1e9
        print(f"At {time_ns} started playing {file_count} random audio files. Playback took {playback_duration} seconds. Total time since request: {request_duration} seconds.\n\n")

        return jsonify(message=f"At {time_ns} started playing {file_count} random audio files. Playback took {playback_duration} seconds. Total time since request: {request_duration} seconds."), 200
    
    except Exception as e:
        print(f"\x1b[2m\x1b[31m    Error occurred: {e}\x1b[0m")
        # write to log file
        with open("logs/" + current_log_file, 'a', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([timestart, "random playback", "error", "N/A"])
        print(f"\x1b[2m    Appended (error) to log file: ./logs/{current_log_file}\x1b[0m")

        return jsonify(error=str(e), message="The server can only play audio reliably at the following sampling rates: 8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000 (Hz). If the error is about weird sample rates, please double check your audio file."), 500