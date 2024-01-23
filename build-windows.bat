@REM For Windows, you must first install ffmpeg and add it to the environment variable.
@echo off
title Building Python Audio Server... - @codynhanpham
call .\venv\Scripts\activate

pyinstaller -F --name py_audio_server --add-binary="bin/async_get.exe;bin" --add-binary="bin/ffmpeg.exe;bin" --add-binary="bin/ffprobe.exe;bin" --hidden-import="scipy.special.cython_special" main.py