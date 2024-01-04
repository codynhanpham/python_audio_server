@REM For Windows, you must first install ffmpeg and add it to the environment variable.

pyinstaller -F --name py_audio_server --add-binary="bin/async_get.exe;bin" main.py