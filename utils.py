from pydub import AudioSegment
import os
import numpy as np
import socket
import contextlib
import os
import sys

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
        print("No audio files found.")
        return {}
    
    audio = {}
    for filename in os.listdir("audio/"):
        if filename.endswith(".wav") or filename.endswith(".mp3"):
            audio[filename] = {
                "name": filename,
                "filename": f"audio/{filename}",
                "audio": AudioSegment.from_file(f"audio/{filename}")
            }

    print(f"Preloaded {len(audio)} audio files to RAM\n")
    return audio



# Generate tones specified in a csv file: frequency (Hz), duration (ms), volume (dB), and sample rate (Hz)
# defaults: 440 Hz, 100 ms, 60 dB, 44100 Hz
def create_tone(frequency=440, duration=100, volume=60, sample_rate=96000):
    # create a tone and convert to the pydub audio segment format
    
    # parse the args and validate their types: freq: float, duration: int, volume: float, sample_rate: int
    try:
        frequency = float(frequency)
    except:
        frequency = 440
        print("Frequency is invalid. Using default value (440 Hz).")

    try:
        duration = int(duration)
    except:
        duration = 100
        print("Duration is invalid. Using default value (100 ms).")
    
    try:
        volume = float(volume)
    except:
        volume = 60
        print("Volume is invalid. Using default value (60 dB).")

    try:
        sample_rate = int(sample_rate)
    except:
        sample_rate = 96000
        print("Sample rate is invalid. Using default value (96000 Hz).")

    # create the tone
    t = np.linspace(0, duration/1000, int(sample_rate * (duration/1000)), dtype=np.float32)
    y = np.sin(frequency * 2 * np.pi * t)
    y *= 10**(volume/20) # convert dB to amplitude
    y /= np.max(np.abs(y)) # normalize to 1.0 range
    y = y.astype(np.float32)

    # convert to audio segment
    tone = AudioSegment(y.tobytes(), frame_rate=sample_rate, sample_width=2, channels=1)
    return tone