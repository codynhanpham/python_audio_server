@REM Create a temporary container to build the project
@REM Using the trusty-python36 image, and the git repo github.com/codynhanpham/python_audio_server

docker run --name python36-audio-server-build-temp -it -v "%cd%:/app" trusty-python36 sh -c "cd /app && git clone https://github.com/codynhanpham/python_audio_server && cd python_audio_server && python3 -m venv venv && source venv/bin/activate && pip3 install -U numpy pydub flask waitress python-dotenv && pip3 install pyinstaller==3.6 && pyinstaller -F --name audio_server main.py" && docker rm python36-audio-server-build-temp