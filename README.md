# Audio via HTTP Request

Play audio on host computer when a remote client makes an HTTP request. The audio start timestamp is logged for future reference.


## Work-in-Progress
- [x] Upgrade project to Python 3.9
- [x] Resample audio files when start up server (to the nearest playable sample rate)
- [x] More efficient way to pre-process audio files for playlist (resample, etc.)
- [x] Preload gapless version of playlist
- [x] Ability to stop audio. Maybe a /stop endpoint
- [x] Sync the playback progress bar with the audio
- [x] Move to using simpleaudio for all audio playback.
- [x] Make it so that only one audio stream is playing at a time.
- [x] Add ability to reload audio files and playlists without restarting the server
- [ ] Smoothing the audio transition between songs in playlist (Eliminate the clicking sound)


## Installation
There are 2 options to install the server: Pre-built binaries (Windows 10+ and Linux 14.04+) and Python.

### Pre-built Binaries
1. Download the latest release from the [releases page](https://github.com/codynhanpham/python_audio_server/releases).
2. Extract the zip file.
3. Run the executable.

Note that to gracefully exit the server, you must press `Ctrl+C` in the terminal window that the server is running in.

### Python
1. Clone the repository.
```bash
git clone https://github.com/codynhanpham/python_audio_server
```
2. Create a virtual environment and install the dependencies.
```bash
cd python_audio_server
python -m venv venv # or python3 -m venv venv

# Linux
source venv/bin/activate
pip3 install -r requirements-linux.txt

# Windows
venv\Scripts\activate
pip install -r requirements-windows.txt
```
3. Run the server.
```bash
python main.py # or python3 main.py
```
Remember that you must start the virtual environment before running the server the next time.
```bash
source venv/bin/activate # Linux
venv\Scripts\activate # Windows
python main.py # or python3 main.py
```

## Usage

**The examples below assume the host IP is `127.0.0.1`, and the server port is `5055`.**

### Endpoints
There are a few endpoints that can be used to control the server.

For the most up-to-date list and documentation, visit the `/docs` endpoint. For example, `http://127.0.0.1:5055/docs`.

~~This repo is the Python implementation of the ***exact same*** project I wrote in Rust. The `README.md` in the Rust repo has more detailed documentation on the endpoints. Check it out at https://github.com/codynhanpham/rust_audio_server~~

This Python version now has a lot more features than the Rust version. The Rust version is no longer maintained, at least for now. The documentation there still serves as a good basis for understanding the endpoints.

#### Common Endpoints
- `/` (home): A client GUI to control the server. This is the easiest way to control the server using the API. You can also use the Inspector to see how the requests are made.
- `/docs`: Get the list of endpoints and the general documentation. Use this to get the most up-to-date list of endpoints and their documentation.
- `/play/{filename}`: Play an audio file. The audio file must be in the `./audio` folder.
- `/playlist/{playlist_name}`: Play a playlist. The playlist must be in the `./playlists` folder.
- `/playlist/gapless/{playlist_name}`: Play a playlist gaplessly. Better than the regular `/playlist` endpoint in most case.
- `/stop`: Stop the audio. All audio streams will be stopped.
- `/info/{filename}`: Get the information of an audio or playlist file.


## Networking
The server can be accessed from remote clients on the same network (same wifi/ethernet) as the host machine. The host machine's IP address can be found using the `ipconfig` command on Windows or the `ifconfig` command on Linux (look for the `IPv4 Address`). In any case, the default local IP is automatically detected and shown when the server is launched. The server port can be changed in the `.env` file.

If the client is on a different network, an easy way to connect is to use [Tailscale](https://tailscale.com/). Tailscale is a peer-to-peer VPN that allows you to connect to your devices from anywhere. It is free for personal use.


## Ubuntu 14.04 Trusty
This Python code is made sure to work on Ubuntu 14.04 Trusty. The easiest way to run this code on Trusty is to use the pre-built binaries. If you want to run the Python code, you will need to install Python. The code is written in Python 3.9, and the bundled executable should be compatible with Trusty.

Navigate to the folder [make-docker-image_trusty-python3.9](/make-docker-image_trusty-python3.9) to see the Dockerfile and the script to build the Docker image. The Docker image is built on Ubuntu 14.04 Trusty and has Python 3.9 installed. The Docker image is used for the PyInstaller to build the pre-built binaries.

Note, the old version of this project used Python 3.6. If you would prefer this for historical reasons, you can still browse files at the last commit before the upgrade to Python 3.9 [here](https://github.com/codynhanpham/python_audio_server/tree/8b46e1b234f78217132723a60f0af6b27d1348f8/make-docker-image_trusty-python3.6).


</br>

## Development
For developing the server and ensuring compatibility with Ubuntu 14.04 Trusty, Docker is used. A convienent Dockerfile is provided in the [make-docker-image_trusty-python3.9](/make-docker-image_trusty-python3.9) folder to build the image from scratch. Furthermore, for reproducibility, the pre-built Docker image is also available on the releases page with the [Docker-Images](https://github.com/codynhanpham/python_audio_server/releases/tag/Docker-Images) tag. This tag will be updated whenever the Docker image used for the pre-built binaries is updated.


### General Use and Testing
If you already have Docker set up, you can either import the Docker image from the releases page or build the Docker image from the Dockerfile. The Docker image is built on Ubuntu 14.04 Trusty and has Python 3.9 installed. The Docker image is used for the PyInstaller to build the pre-built binaries.

After you have the Docker image loaded, there is also a `.bat` script for Windows to quickly run the image in a container that will mounts the project folder. Simply clone this repo, `cd` into it, and run the [`docker-terminal.bat`](/docker-terminal.bat) file. This will open a terminal in the container with the project folder mounted in `/app`. You can then use the terminal as you would a normal Ubuntu 14.04 Trusty machine. The terminal will have Python 3.9 installed, and you can use the virtual environment to run the server.

Workflow on Windows to run the project in Docker:
```batch
git clone https://github.com/codynhanpham/python_audio_server.git
cd python_audio_server

:: Options: Load the Docker image or build it from the Dockerfile

:: 1. If Build from Dockerfile:
cd make-docker-image_trusty-python3.9
docker build -t trusty-python3.9 .

:: 2. If Load from Releases:
:: (First, download the Docker image from the releases page)
:: wget ... (or use the browser to download the tar.gz file)
docker load -i trusty-python3.9.tar.gz


:: After you have the Docker image ready, the docker-terminal.bat script can be used anytime after this
:: Run the Docker container with the project folder mounted
:: (still inside of the python_audio_server project folder)
./docker-terminal.bat


:: Now, you are in Ubuntu 14.04 Trusty with Python 3.9 installed. That's it!

:: Inside the container, remember to start the virtual environment first!!!
python3.9 -m venv venv
source venv/bin/activate

:: Do whatever test or development you need to do


:: Ctrl + D to exit the container, this container will be automatically removed
```

### Bundling
To ensure backward compatibility with Ubuntu 14.04, the pre-built binaries are built using PyInstaller in the Docker container on Ubuntu 14.04 Trusty.

After getting the Docker image set up, a convienent [`build-ubuntu.bat`](/build-ubuntu.bat) script is provided to bundle the app with Docker. **Note that using the script, most packages will be installed with their latest version. For a more predictable build, run a manual package installation first before building with the script.** (The script was designed to be used after the manual package installation. The pip install commands in the script were used to make sure all essential packages were installed, that's about it.)

Workflow on Windows to bundle the project with Docker:
```batch
:: Clone the project and set up Docker as mentioned above


:: First time setup: Install the packages manually
./docker-terminal.bat
python3.9 -m venv linux-venv
source linux-venv/bin/activate
pip install -r requirements-linux.txt

:: Ctrl + D to exit the container, this container will be automatically removed
:: The linux-venv folder will be created in the project folder


:: Now (and anytime after this point), you can use the build-ubuntu.bat script to bundle the app
./build-ubuntu.bat


:: After this, for rebuilding the app, you can just run the script ./build-ubuntu.bat script again
```