@REM Create a temporary container to build the project
@REM Using the trusty-python39 image, and the git repo github.com/codynhanpham/python_audio_server

@REM Use this command to build the project with SimpleAudio and FFmpeg
@REM Just in case PyInstaller cannot find .so libs files, copy the scipy.libs folder (inside of linux-venv/lib/python3.7/site-packages) to the bin folder here
@REM docker run --name python39-audio-server-build-temp -v "%cd%:/app" trusty-python39 /bin/sh -c "cd /app && python3.9 -m venv linux-venv && . linux-venv/bin/activate && pip3 install --upgrade setuptools  && pip3 install numpy simpleaudio numba resampy pyserial argparse pydub flask waitress python-dotenv scipy && pip3 install pyinstaller && pip3 freeze > requirements_linux.txt && export PATH=\"/app/bin/scipy.libs:$PATH\" && export PATH=\"/app/bin:$PATH\" && pyinstaller -y --name audio_server --add-binary=\"bin/ffmpeg:bin\" --add-binary=\"bin/ffprobe:bin\" --add-binary=\"bin/async_get.exe:bin\" --hidden-import=\"scipy.special.cython_special\" --add-data=\"static/*:static\" main.py" && docker rm python39-audio-server-build-temp


docker run --name python39-audio-server-build-temp -v "%cd%:/app" trusty-python39 /bin/sh -c "cd /app && python3.9 -m venv linux-venv && . linux-venv/bin/activate && pip3 install --use-pep517 -r requirements_linux.txt && export PATH=\"/app/bin/scipy.libs:$PATH\" && export PATH=\"/app/bin:$PATH\" && pyinstaller -y --name audio_server --add-binary=\"bin/ffmpeg:bin\" --add-binary=\"bin/ffprobe:bin\" --add-binary=\"bin/async_get.exe:bin\" --hidden-import=\"scipy.special.cython_special\" --add-data=\"static/*:static\" main.py" && docker rm python39-audio-server-build-temp