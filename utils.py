from pydub import AudioSegment
import os
import numpy as np
import socket
import contextlib
import os
import sys
from scipy.signal import chirp

import time
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

PLAYLIST = {}
SHUTDOWN_TOKENS = []

@contextlib.contextmanager
def ignore_stderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)


def resource_path(relative_path=''):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

 
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # any IP address will do...
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP



# a function to load and process audio files in audio/ directory
def load_audio(CLI_ARGS):
    print("Preloading audio files in ./audio/*.wav ...")

    # if audio/ directory doesn't exist, show a warning and return an empty dict
    if not os.path.exists("audio/"):
        print("\x1b[2m\x1b[31m    Error: Audio folder not found. Play functions will not work for this session.\x1b[0m")
        return {}
    
    audio = {}
    audio_types = [".wav", ".mp3", ".flac", ".ogg"]
    for filename in os.listdir("audio/"):
        if filename.endswith(tuple(audio_types)):
            extension = filename.split(".")[-1]
            audio_segment = AudioSegment.from_file(f"audio/{filename}", format=extension)

            # create the info string
            info = f"filename: {filename}\n"
            info += f"duration: {len(audio_segment)} ms\n"
            info += f"channels: {audio_segment.channels}\n"
            info += f"sample_rate: {audio_segment.frame_rate} Hz\n"

            if audio_segment.sample_width > 2:
                print(f"\x1b[2m\x1b[33m    Warning (\"{filename}\"): bit depth > 16 bit may not playback correctly.\x1b[0m")
                # audio_segment = audio_segment.set_sample_width(2)

                # if CLI_ARGS.no_convert_to_s16 is false, auto convert to 16-bit signed integer format for reliability
                if not CLI_ARGS.no_convert_to_s16:
                    audio_segment = audio_segment.set_sample_width(2)
                    print(f"\x1b[2m\x1b[34m    Converting \"{filename}\" to 16-bit signed integer format...\x1b[0m")


            audio[filename] = {
                "name": filename,
                "filename": f"audio/{filename}",
                "audio": audio_segment,
                "info": info
            }

    print(f"Preloaded {len(audio)} audio files to RAM\n")
    return audio


# a function to load and validate + process playlist files in playlists/ directory
def load_and_validate_playlists(playlist_folder_path, AUDIO):
    # if no playlist folder is found, skip loading playlists
    if not os.path.exists(playlist_folder_path):
        return {}

    print("Loading playlist files in ./playlists/*.txt ...")

    # Playlist: Key is the name of the file.txt, Value is a Vec of {type: "audio" or "pause", value: "filename" or "pause_duration in ms"}

    playlists = {}
    for filename in os.listdir(playlist_folder_path):
        if not filename.endswith(".txt"):
            continue

        playlist = []
        error_occurred = False
        raw_playlist_text = ""
        with open(f"{playlist_folder_path}/{filename}", "r") as f:
            raw_playlist_text = f.read()
            for line in raw_playlist_text.split("\n"):
                line = line.strip()
                if line.startswith("#") or line == "":
                    continue

                if line.startswith("pause_") and line.endswith("ms"):
                    # pause format is pause_{duration in ms}ms
                    try:
                        int(line.split("_")[1][:-2])
                        playlist.append({
                        "type": "pause",
                        "value": int(line.split("_")[1][:-2])
                    })
                    except:
                        parsed = line.split("_")[1][:-2]
                        print(f"\x1b[2m\x1b[31m    Error: Pause duration \"{parsed}\" is not a valid integer\x1b[0m")
                        print(f"\x1b[2m    Ignoring playlist \"{filename}\"...\n\x1b[0m")
                        error_occurred = True
                        break
                elif line in AUDIO:
                    playlist.append({
                        "type": "audio",
                        "value": line
                    })
                else:
                    print(f"\x1b[2m\x1b[31m    Error: Audio file \"{line}\" not found\x1b[0m")
                    print("\x1b[2m    Please make sure the audio file exists in the \"audio\" folder and try again.\x1b[0m")
                    print(f"\x1b[2m    Ignoring playlist \"{filename}\"...\n\x1b[0m");
                    error_occurred = True
                    break

        if error_occurred or not playlist:
            continue

        # calculate the total duration of the playlist
        total_duration = 0
        audio_count = 0
        pause_count = 0
        for step in playlist:
            if step["type"] == "audio":
                total_duration += len(AUDIO[step["value"]]["audio"])
                audio_count += 1
            elif step["type"] == "pause":
                total_duration += step["value"]
                pause_count += 1

        info = f"playlist name: {filename}\n"
        info += f"* total duration: {total_duration} ms\n"
        info += f"steps: {len(playlist)}\n"
        info += f"  - audio steps: {audio_count}\n"
        info += f"  - pause steps: {pause_count}\n\n"

        # also add the playlist text to the info string
        info += "playlist data:\n"
        # tab the playlist text by 4 spaces
        info += "\n".join(["    " + line for line in raw_playlist_text.split("\n")])
        info += "\n\n\n"
        info += "* 'total duration'  is an estimated value made by adding the duration of each audio file and pause duration in the playlist. This value should be fairly accurate if the playlist is played gaplessly. Otherwise, the real-world duration will be a bit longer, due to the time it takes to switch between audio files.\n\n"

        playlists[filename] = {
            "name": filename,
            "data": playlist,
            "info": info
        }


    print(f"Loaded {len(playlists)} playlist files\n")
    return playlists

def create_tone(frequency=440, duration=100, volume=60, sample_rate=192000, edge=0):
    # create a tone and convert to the pydub audio segment format
    
    # parse the args and validate their types: freq: float, duration: int, volume: float, sample_rate: int, edge: int (positive or negative)
    try:
        frequency = float(frequency)
    except:
        frequency = 440
        print("\x1b[2m\x1b[31m    Frequency is invalid. Using default value (440 Hz).")

    try:
        duration = int(duration)
    except:
        duration = 100
        print("\x1b[2m\x1b[31m    Duration is invalid. Using default value (100 ms).")
    
    try:
        volume = float(volume)
    except:
        volume = 60
        print("\x1b[2m\x1b[31m    Volume is invalid. Using default value (60 dB).")

    try:
        sample_rate = int(sample_rate)
    except:
        sample_rate = 192000
        print("\x1b[2m\x1b[31m    Sample rate is invalid. Using default value (192000 Hz).")

    try:
        edge = int(edge)
    except:
        edge = 0
        print("\x1b[2m\x1b[31m    Edge is invalid. Using default value (0 ms).")

    if edge < 0 and duration < 2*edge:
        edge = 0
        print("\x1b[2m\x1b[31m    Edge is negative but Duration is < 2*Edge. Using default value for edge (0 ms).")

    # modify the total duration if edge is specified:
    # edge < 0: the ramp duration is already included in the duration --> no modification
    # edge > 0: the ramp duration is not included in the duration --> add the ramp duration (2 * edge) to the duration
    if edge > 0:
        duration += 2 * edge

    # create the tone at the specified frequency and sample rate
    samples = int(sample_rate * duration / 1000)
    # calculate the x values
    x = np.arange(samples)
    # calculate the y values
    y = np.sin(2 * np.pi * frequency * x / sample_rate)
    # scale the y values
    y *= 10 ** (volume / 20)
    
    # Add edge (raise and fall) to the tone
    if edge != 0:
        # calculate the number of edge samples
        edge_samples = int(sample_rate * abs(edge) / 1000)

        # create the fade-in and fade-out ramps
        fade_in = np.linspace(0, 1, edge_samples)
        fade_out = fade_in[::-1]

        # apply the fade-in and fade-out
        y[:edge_samples] *= fade_in
        y[-edge_samples:] *= fade_out

    # convert to 16-bit data
    y = y.astype(np.int16)

    # convert to audio segment
    tone = AudioSegment(y.tobytes(), frame_rate=sample_rate, sample_width=2, channels=1)
    return tone



def create_sweep(mode: str, start_frequency=440, end_frequency=440, duration=100, volume=60, sample_rate=192000, edge=0):
    # For sweep, edge must be negative since we cannot extend the duration of the sweep as limited by the start and end frequencies

    # Parse the args and validate their types
    try:
        start_frequency = float(start_frequency)
        end_frequency = float(end_frequency)
        if not (0 <= start_frequency <= 200_000) or not (0 <= end_frequency <= 200_000):
            raise ValueError
    except:
        start_frequency = 440
        end_frequency = 8800
        print("\x1b[2m\x1b[31m    Frequency is invalid. Using default value (440-8800 Hz).")

    try:
        duration = int(duration)
    except:
        duration = 100
        print("\x1b[2m\x1b[31m    Duration is invalid. Using default value (100 ms).")
    
    try:
        volume = float(volume)
    except:
        volume = 60
        print("\x1b[2m\x1b[31m    Volume is invalid. Using default value (60 dB).")

    try:
        sample_rate = int(sample_rate)
    except:
        sample_rate = 192000
        print("\x1b[2m\x1b[31m    Sample rate is invalid. Using default value (192000 Hz).")

    # Parse the mode: "linear", "quadratic", "logarithmic", "hyperbolic"
    if mode not in ["linear", "quadratic", "logarithmic", "hyperbolic"]:
        mode = "linear"
        print("\x1b[2m\x1b[31m    Mode is invalid. Using default value (linear).")

    try:
        edge = int(edge)
        # edge also needs to be negative
        if edge > 0:
            raise ValueError
    except:
        edge = 0
        print("\x1b[2m\x1b[31m    Edge for sweep is invalid. Using default value (0 ms).")

    if edge < 0 and duration < 2*abs(edge):
        edge = 0
        print("\x1b[2m\x1b[31m    Edge is negative but Duration is < 2*Edge. Using default value for edge (0 ms).")

    # Create the sweep at the specified frequency and sample rate
    t = np.linspace(0, duration / 1000, duration * sample_rate // 1000)
    # Calculate the y values
    y = chirp(t, start_frequency, duration / 1000, end_frequency, method=mode)
    # Scale the y values
    y *= 10 ** (volume / 20)

    # Add edge (raise and fall) to the tone
    if edge != 0:
        # calculate the number of edge samples
        edge_samples = int(sample_rate * abs(edge) / 1000)

        # create the fade-in and fade-out ramps
        fade_in = np.linspace(0, 1, edge_samples)
        fade_out = fade_in[::-1]

        # apply the fade-in and fade-out
        y[:edge_samples] *= fade_in
        y[-edge_samples:] *= fade_out


    # Convert to 16-bit data
    y = y.astype(np.int16)

    # Convert to audio segment
    tone = AudioSegment(y.tobytes(), frame_rate=sample_rate, sample_width=2, channels=1)
    return tone


# a class to create and handle expiring of variables --> use for creating and handling of tokens
class ExpiringVariable:
    def __init__(self, value, timeout=60):
        self.value = value
        self._last_updated = time.time()
        self.timeout = timeout # in seconds

    @property
    def value(self):
        """Get the value if the value hasn't timed out.
        Returns None if the value has timed out."""
        if time.time() - self._last_set < self.timeout:
            return self._value
        else:
            return None
        
    @value.setter
    def value(self, value, timeout=None):
        """Set the value and update the last updated time."""
        self._value = value
        self._last_set = time.time()
        if timeout is not None:
            self.timeout = timeout