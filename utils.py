from pydub import AudioSegment
import os
import numpy as np

# a function to load and process audio files in audio/ directory
def load_audio():
    print("Loading audio files...")
    
    audio = {}
    for filename in os.listdir("audio/"):
        if filename.endswith(".wav") or filename.endswith(".mp3"):
            name = filename.split(".")[0]
            audio[name] = {
                "name": name,
                "filename": f"audio/{filename}",
                "audio": AudioSegment.from_file(f"audio/{filename}")
            }

    print(f"Loaded {len(audio)} audio files")
    return audio

# Generate tones specified in a csv file: frequency (Hz), duration (ms), volume (dB), and sample rate (Hz)
# defaults: 440 Hz, 100 ms, 60 dB, 44100 Hz



def create_tone(frequency=440, duration=100, volume=60, sample_rate=44100):
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
        sample_rate = 44100
        print("Sample rate is invalid. Using default value (44100 Hz).")

    # create the tone
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