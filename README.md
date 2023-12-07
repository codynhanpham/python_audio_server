# Audio via HTTP Request

Play audio on host computer when a remote client makes an HTTP request. The audio start timestamp is logged for future reference.

## Installation
There are 2 options to install the server: Windows executable and Python.

### Windows Executable
1. Download the latest release for Windows machine from the [releases page](https://github.com/codynhanpham/python_audio_server/releases/). There should be 2 executables: `audio_server.exe` and `generate_bat_files.exe`, along with a folder `audio/` where you would put your audio files. The 3 files/folders must be in the same directory.
2. The `generate_bat_files.exe` is used to generate the batch files that request the audio files. The resulting batch files can be saved to the remote client's machine and run to make the HTTP request. 
3. On the host machine, run `generate_bat_files.exe` to start the server. The server port (*default: `5055`*) and the log file prefix (*default: `log_`*) can be changed in the `.env` file. The log file will be saved in the `logs/` folder in the same directory as the executable.

### Python
1. Clone the repository.
```bash
git clone https://github.com/codynhanpham/python_audio_server
```
2. Create a virtual environment and install the dependencies.
```bash
cd python_audio_server
python -m venv venv
source venv/bin/activate # Linux
venv\Scripts\activate # Windows
pip install -r requirements.txt
```
3. Run the server.
```bash
python main.py
```
Remember that you must start the virtual environment before running the server the next time.
```bash
source venv/bin/activate # Linux
venv\Scripts\activate # Windows
python main.py
```

## Usage

**The examples below assume the host IP is `127.0.0.1`, and the server port is `5055`.**

### Endpoints
#### `/ping`
Returns `pong` if the server is running.

Example:
```bash
curl http://127.0.0.1:5055/ping
```

#### `/play/<audio_file>`
Plays the audio file `<audio_file>` in the `audio/` folder. `<audio_file>` is the audio file name without the extension in the `audio` folder.

Example:

To play a file named `doorbell.wav` in the `audio/` folder, make a request to the following endpoint:

```bash
curl http://127.0.0.1:5055/play/doorbell
```

#### `/startnewlog`
Starts a new log file. Requests from this point on will be logged in a new file. Logs are saved in the `logs/` folder in the same directory as the executable.

The log file name is in the format `<log_file_prefix><timestamp>.csv`. `<log_file_prefix>` is the log file prefix in the `.env` file. `<timestamp>` is the current timestamp in the format `YYYY-MM-DD_HH-MM-SS`.

The `csv` log has 3 columns:
- `timestamp`: The epoch timestamp of the request in nano seconds.
- `audio_file`: The audio file name.
- `status`: The status of the request. Either `success` or `error`.

Example:
```bash
curl http://127.0.0.1:5055/startnewlog
```

### Batch Files
Batch files that make the HTTP request to play the audio files can be generated using the `generate_bat_files.exe` executable. The batch files can be saved to the remote client's machine and run to make the HTTP request.

These provide a quick and simple way to play audio on the host machine from a remote client.

The batch files are generated in the `bat_files` folder in the same directory as the executable. These files are Host IP and Port specific. The individual `.bat` files are saved under `bat_files/<host_ip>_<host_port>/` folder.

There are 2 types of batch files:
- `<audio_file>.bat`: Plays the audio file `<audio_file>` in the `audio` folder. `<audio_file>` is the audio file name without the extension in the `audio` folder.
- `start_new_log.bat`: Starts a new log file. Requests from this point on will be logged in a new file.

## Networking
The server can be accessed from remote clients on the same network (same wifi/ethernet) as the host machine. The host machine's IP address can be found using the `ipconfig` command on Windows or the `ifconfig` command on Linux (look for the `IPv4 Address`). The server port can be changed in the `.env` file.

If the client is on a different network, an easy way to connect is to use [Tailscale](https://tailscale.com/). Tailscale is a peer-to-peer VPN that allows you to connect to your devices from anywhere. It is free for personal use.