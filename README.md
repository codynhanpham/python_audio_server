# Audio via HTTP Request

Play audio on host computer when a remote client makes an HTTP request. The audio start timestamp is logged for future reference.


## Work-in-Progress
- [x] Upgrade project to Python 3.7
- [x] Resample audio files when start up server (to the nearest playable sample rate)
- [x] More efficient way to pre-process audio files for playlist (resample, etc.)
- [x] Preload gapless version of playlist
- [ ] Move to using simpleaudio for all audio playback. Make it so that only one audio stream is playing at a time.
- [ ] Add ability to reload audio files and playlists without restarting the server
- [ ] Smoothing the audio transition between songs in playlist (Eliminate the clicking sound)
- [ ] Ability to stop audio. Maybe a /stop endpoint
- [ ] Sync the playback progress bar with the audio


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

For the most up-to-date list and documentation, visit the `/` (home) endpoint. For example, `http://127.0.0.1:5055/`.

This repo is the Python implementation of the ***exact same*** project I wrote in Rust. The `README.md` in the Rust repo has more detailed documentation on the endpoints. Check it out at https://github.com/codynhanpham/rust_audio_server

## Networking
The server can be accessed from remote clients on the same network (same wifi/ethernet) as the host machine. The host machine's IP address can be found using the `ipconfig` command on Windows or the `ifconfig` command on Linux (look for the `IPv4 Address`). In any case, the default local IP is automatically detected and shown when the server is launched. The server port can be changed in the `.env` file.

If the client is on a different network, an easy way to connect is to use [Tailscale](https://tailscale.com/). Tailscale is a peer-to-peer VPN that allows you to connect to your devices from anywhere. It is free for personal use.


## Ubuntu 14.04 Trusty
This Python code is made sure to work on Ubuntu 14.04 Trusty. The easiest way to run this code on Trusty is to use the pre-built binaries. If you want to run the Python code, you will need to install Python. The code is written in Python 3.7, and the bundled executable should be compatible with Trusty.

Navigate to the folder [make-docker-image_trusty-python3.7](/make-docker-image_trusty-python3.7) to see the Dockerfile and the script to build the Docker image. The Docker image is built on Ubuntu 14.04 Trusty and has Python 3.7 installed. The Docker image is used for the PyInstaller to build the pre-built binaries.

Note, the old version of this project used Python 3.6. If you would prefer this for historical reasons, you can still browse files at the last commit before the upgrade to Python 3.7 [here](https://github.com/codynhanpham/python_audio_server/tree/8b46e1b234f78217132723a60f0af6b27d1348f8/make-docker-image_trusty-python3.6).