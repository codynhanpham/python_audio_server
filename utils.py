from pydub import AudioSegment
import os
import numpy as np
import socket
import contextlib
import os
import sys
from sympy import symbols, parse_expr, lambdify
from scipy.signal import chirp

PLAYLIST = {}

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
def load_audio():
    print("Preloading audio files in ./audio/*.wav ...")

    # if audio/ directory doesn't exist, show a warning and return an empty dict
    if not os.path.exists("audio/"):
        print("\x1b[2m\x1b[31m    Error: Audio folder not found. Play functions will not work for this session.\x1b[0m")
        return {}
    
    audio = {}
    audio_types = [".wav", ".mp3", ".flac", ".ogg"]
    for filename in os.listdir("audio/"):
        if filename.endswith(tuple(audio_types)):
            audio[filename] = {
                "name": filename,
                "filename": f"audio/{filename}",
                "audio": AudioSegment.from_file(f"audio/{filename}")
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
        with open(f"{playlist_folder_path}/{filename}", "r") as f:
            for line in f:
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

        playlists[filename] = playlist

    print(f"Loaded {len(playlists)} playlist files\n")
    return playlists

# Generate tones specified in a csv file: frequency (Hz), duration (ms), volume (dB), and sample rate (Hz)
# defaults: 440 Hz, 100 ms, 60 dB, 96000 Hz
def create_tone(frequency=440, duration=100, volume=60, sample_rate=192000):
    # create a tone and convert to the pydub audio segment format
    
    # parse the args and validate their types: freq: float, duration: int, volume: float, sample_rate: int
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

    # create the tone at the specified frequency and sample rate
    samples = int(sample_rate * duration / 1000)
    # calculate the x values
    x = np.arange(samples)
    # calculate the y values
    y = np.sin(2 * np.pi * frequency * x / sample_rate)
    # scale the y values
    y *= 10 ** (volume / 20)
    # convert to 16-bit data
    y = y.astype(np.int16)

    # convert to audio segment
    tone = AudioSegment(y.tobytes(), frame_rate=sample_rate, sample_width=2, channels=1)
    return tone




# Generate tones specified in a csv file: frequency (Hz), duration (ms), volume (dB), and sample rate (Hz)
# defaults: 440 Hz, 100 ms, 60 dB, 96000 Hz
def create_sweep(mode: str, start_frequency=440, end_frequency=440, duration=100, volume=60, sample_rate=192000):
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

    # Create the sweep at the specified frequency and sample rate
    t = np.linspace(0, duration / 1000, duration * sample_rate // 1000)
    # Calculate the y values
    y = chirp(t, start_frequency, duration / 1000, end_frequency, method=mode)
    # Scale the y values
    y *= 10 ** (volume / 20)
    # Convert to 16-bit data
    y = y.astype(np.int16)

    # Convert to audio segment
    tone = AudioSegment(y.tobytes(), frame_rate=sample_rate, sample_width=2, channels=1)
    return tone

def save_sweep(sweep_function: str, start_frequency=440, end_frequency=440, duration=100, volume=60, sample_rate=192000, filename="sweep.wav"):
    tone = create_sweep(sweep_function, start_frequency, end_frequency, duration, volume, sample_rate)
    tone.export(filename, format="wav")