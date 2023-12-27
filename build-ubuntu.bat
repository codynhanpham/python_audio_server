@REM Create a temporary container to build the project
@REM Using the trusty-python36 image, and the git repo github.com/codynhanpham/python_audio_server

@REM Use this command to build the project with PyAudio and FFmpeg
docker run --name python36-audio-server-build-temp -it -v "%cd%:/app" trusty-python36 /bin/sh -c "cd /app && python3 -m venv linux-venv && . linux-venv/bin/activate && pip3 install -U numpy PyAudio==0.2.14 pydub flask waitress python-dotenv && pip3 install pyinstaller==3.6 && pyinstaller -F --name py_audio_server --add-binary=\"bin/ffmpeg:.\" --add-binary=\"bin/ffprobe:.\" main.py && pip3 freeze > requirement_linux.txt" && docker cp python36-audio-server-build-temp:/app/dist . && docker rm python36-audio-server-build-temp

@REM Use this command to build the project with SimpleAudio and FFmpeg (more stable, but can't handle weird audio sample rates)
:: docker run --name python36-audio-server-build-temp -it -v "%cd%:/app" trusty-python36 /bin/sh -c "cd /app && python3 -m venv linux-venv && . linux-venv/bin/activate && pip3 install -U numpy simpleaudio pydub flask waitress python-dotenv && pip3 install pyinstaller==3.6 && pyinstaller -F --name py_audio_server --add-binary=\"bin/ffmpeg:.\" main.py && pip3 freeze > requirement_linux.txt" && docker cp python36-audio-server-build-temp:/app/dist . && docker rm python36-audio-server-build-temp