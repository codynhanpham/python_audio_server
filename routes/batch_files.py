from flask import Blueprint, jsonify, g, send_file
from textwrap import dedent

import time,os
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

from zipfile import ZipFile
import io

import utils as utils

def create_batch_file(file_name, host_ip, port, with_async, route):
    # 2 different templates for the batch file, depending on whether we want to use async or not
    if with_async:
        batch_file = f"""\
            @echo off\n\
            .\\async_get.exe -u http://{host_ip}:{port}/{route}/{file_name}\n\
            exit\n
        """
    else:
        batch_file = f"""\
            @echo off\n\
            <!-- :\n\
            for /f \"tokens=* usebackq\" %%a in (`start /b cscript //nologo \"%~f0?.wsf\"`) do (set timestamp=%%a)\n\
            curl -X GET http://{host_ip}:{port}/{route}/{file_name}?time=%timestamp%000000\n\
            exit /b\n\
            -->\n\
            \n\
            <job><script language=\"JavaScript\">\n\
            WScript.Echo(new Date().getTime());\n\
            </script></job>\n
        """

    return dedent(batch_file)


def create_batch_file_zip(audio_files, playlists, host_ip, port, with_async):
    # Return the zip file name and the io.BytesIO object of the zip file
    # zip file name would be {host_ip}_{port} or {host_ip}_{port}_async .zip
    zip_file_name = (f"{host_ip}_{port}" if not with_async else f"{host_ip}_{port}_async") + ".zip"

    # make list of file names from audio_files and playlists
    audio_file_names = [audio_file for audio_file in audio_files]
    playlist_file_names = [playlist for playlist in playlists]

    # create the batch files for each audio file and playlist, add to the zip file
    zip_data = io.BytesIO()
    with ZipFile(zip_data, 'w') as zip_file:
        for audio_file_name in audio_file_names:
            batch_file = create_batch_file(audio_file_name, host_ip, port, with_async, "play")
            zip_file.writestr(audio_file_name + ".bat", batch_file)

        for playlist_file_name in playlist_file_names:
            batch_file = create_batch_file(playlist_file_name, host_ip, port, with_async, "playlist")
            zip_file.writestr(playlist_file_name + ".bat", batch_file)

        # create the batch file to start a new log, add to the zip file
        batch_file = f"""\
            @echo off\n\
            curl -X GET http://{host_ip}:{port}/startnewlog\n\
            exit\n
        """
        zip_file.writestr("startnewlog.bat", dedent(batch_file))

        # add async_get.exe to the zip file if with_async is True
        if with_async:
            # path to the async_get.exe file from resources base path
            async_get_path = os.path.join(g.BASE_PATH, "bin", "async_get.exe")
            
            zip_file.write(async_get_path, "async_get.exe")

    zip_data.seek(0)

    return {"zip_file_name": zip_file_name, "data": zip_data}



batch_file_blueprint = Blueprint('batch_file', __name__)

@batch_file_blueprint.route('/generate_batch_files', methods=['GET'])
def generate_batch_files():
    time_ns = time.time_ns()
    print(f"{time_ns}: Received /generate_batch_files")

    AUDIO = g.AUDIO
    PLAYLIST = g.PLAYLIST
    PORT = g.PORT
    IP_ADDRESS = g.IP_ADDRESS

    if not AUDIO and not PLAYLIST:
        print(f"\x1b[2m\x1b[31m    No audio file or playlist found\x1b[0m")
        return jsonify(error="No audio file (.wav or .mp3) in the ./audio/ folder, as well as no valid playlist file (.txt) in the ./playlists/ folder."), 404

    # generate the batch files for each audio file and playlist, as well as the batch file to start a new log
    # return as a zip file for the user to download
    # zip file name would be {host_ip}_{port}.zip
    zip_file = create_batch_file_zip(AUDIO, PLAYLIST, IP_ADDRESS, PORT, False)

    return send_file(
        zip_file["data"],
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename=zip_file["zip_file_name"]
    )


@batch_file_blueprint.route('/generate_batch_files_async', methods=['GET'])
def generate_batch_files_async():
    # Similar to generate_batch_files, but with async_get.exe instead of curl
    # only different is also bundle async_get.exe with the zip file
    time_ns = time.time_ns()
    print(f"{time_ns}: Received /generate_batch_files_async")

    AUDIO = g.AUDIO
    PLAYLIST = g.PLAYLIST
    PORT = g.PORT
    IP_ADDRESS = g.IP_ADDRESS

    if not AUDIO and not PLAYLIST:
        print(f"\x1b[2m\x1b[31m    No audio file or playlist found\x1b[0m")
        return jsonify(error="No audio file (.wav or .mp3) in the ./audio/ folder, as well as no valid playlist file (.txt) in the ./playlists/ folder."), 404
    
    # generate the batch files for each audio file and playlist, as well as the batch file to start a new log
    # return as a zip file for the user to download
    # zip file name would be {host_ip}_{port}_async.zip
    zip_file = create_batch_file_zip(AUDIO, PLAYLIST, IP_ADDRESS, PORT, True)

    return send_file(
        zip_file["data"],
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename=zip_file["zip_file_name"]
    )
