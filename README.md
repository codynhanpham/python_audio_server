# Audio via HTTP Request

Play audio on host computer when a remote client makes an HTTP request. The audio start timestamp is logged for future reference.

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
This Python code is made sure to work on Ubuntu 14.04 Trusty. The easiest way to run this code on Trusty is to use the pre-built binaries. If you want to run the Python code, you will need to install Python 3.6.

As you may know, Trusty is old and the PPA for Python 3.6 is not available anymore anywhere (I looked around, yes, for a few hours). To install Python 3.6, you will need to build it from source. I have created a Dockerfile that will help you create a Docker image with Python 3.6 installed. From there, you can clone the repo, then run the `build-ubuntu.bat` file I included to build the code.

The Dockerfile is located in the [`make-docker-image_trusty-python3.6` directory](/make-docker-image_trusty-python3.6/). Follow the instructions in the README file to build the Docker image.