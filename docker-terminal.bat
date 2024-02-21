@REM Run this batch file to start the container from the trusty-python37 image
@REM This will also mount the current directory to the /app directory in the container

@REM Print note to user on how to stop the container before starting it
@echo off
echo:
echo To stop the container, press Ctrl+D. The container will be removed automatically.
echo:
echo:

@REM Start the container, then cd to the /app directory
docker run --name python39-interactive -it -p 5057:5055 -v "%cd%:/app" trusty-python39 /bin/bash -c "cd /app && /bin/bash"

@REM To access the server from the host machine, the port is 5057 (not 5055, that is reserved in case you do something else with the code while the container is running/idle)

@REM If the container is stopped, remove it
docker rm python39-interactive
