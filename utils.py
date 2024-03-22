from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from pydub import AudioSegment
import os
import numpy as np
import socket
import contextlib
import sys
import resampy
from scipy.signal import chirp
import simpleaudio
from time import sleep
import math, shutil
import serial
from dotenv import dotenv_values

import time
if not hasattr(time, 'time_ns'):
    time.time_ns = lambda: int(time.time() * 1e9)

PLAYLIST = {}
AUDIO = {}
SHUTDOWN_TOKENS = []
PLAYLIST_ABORT = False

config = dotenv_values(".env")
BAUDRATE = int(config.get("BAUDRATE", 9600))
SERIAL_PORT = config.get("SERIAL_PORT", "COM3")
PULSE_BYTE_COUNT = int(config.get("PULSE_BYTE_COUNT", 1))

def start_serial_device():
    global SerialDevice
    # try to set serial Device, if no serial device is found, set SerialDevice to None
    try:
        SerialDevice = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
        print(f"\x1b[1m\x1b[32m\n\nSerial device found at {SERIAL_PORT} (baudrate: {BAUDRATE})\x1b[0m")
        print(f"\x1b[1m\x1b[32m    --> Connected\x1b[0m")
    except:
        SerialDevice = None

    return SerialDevice

SERIAL_DEVICE = start_serial_device()


_DEFAULT_POOL = ThreadPoolExecutor()

def threadpool(f, executor=None):
    @wraps(f)
    def wrap(*args, **kwargs):
        return (executor or _DEFAULT_POOL).submit(f, *args, **kwargs)

    return wrap

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


def audiosegment_to_librosawav(audiosegment):
    """Used by librosa and resampy"""
    channel_sounds = audiosegment.split_to_mono()
    samples = [s.get_array_of_samples() for s in channel_sounds]

    fp_arr = np.array(samples).T.astype(np.float32)
    fp_arr /= np.iinfo(samples[0].typecode).max
    fp_arr = fp_arr.reshape(-1)

    return fp_arr


def resample_audio(audio_segment: AudioSegment, new_sample_rate: int):
    """Need to `import resampy` to use this. Resample the audio segment to the new sample rate using `resampy` https://resampy.readthedocs.io/en/stable/."""
    
    resample_type = "sinc_window"

    # use librosa to resample the audio segment to the new sample rate
    y = audiosegment_to_librosawav(audio_segment)

    # Check if the audio is stereo
    if audio_segment.channels == 2:
        # Split the stereo audio into two mono audios
        y_left = y[0::2]
        y_right = y[1::2]

        # Resample both channels separately
        y_left = resampy.resample(y_left, audio_segment.frame_rate, new_sample_rate, filter=resample_type)
        y_right = resampy.resample(y_right, audio_segment.frame_rate, new_sample_rate, filter=resample_type)

        # Combine the two channels back into stereo
        y = np.vstack((y_left, y_right)).flatten('F')
    else:
        # If the audio is mono, just resample it
        y = resampy.resample(y, audio_segment.frame_rate, new_sample_rate, filter=resample_type)

    # convert the resampled audio back to AudioSegment
    y = (y * np.iinfo(np.int16).max).astype(np.int16)
    audio_segment = AudioSegment(y.tobytes(), frame_rate=new_sample_rate, sample_width=2, channels=audio_segment.channels)

    return audio_segment



def create_tone(frequency=440, duration=100, volume=60, sample_rate=192000, edge=0, channels=1):
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

    # limit channels to 1 or 2
    if channels not in [1, 2]:
        channels = 1
        print("\x1b[2m\x1b[31m    Channels is invalid. Using default value (1).\x1b[0m")


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

    # duplicate the tone to the number of channels
    y = np.tile(y, channels)

    # convert to audio segment
    tone = AudioSegment(y.tobytes(), frame_rate=sample_rate, sample_width=2, channels=channels)
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


            # only work with 1 or 2 channels
            if audio_segment.channels > 2:
                print(f"\x1b[2m\x1b[31m    Error: \"{filename}\" has more than 2 channels. Only 1 or 2 channels (mono or stereo) are supported.\x1b[0m")
                print(f"\x1b[2m\x1b[31m    Ignoring \"{filename}\"...\n\x1b[0m")
                continue


            # create the info string
            info = f"filename: {filename}\n"
            info += f"duration: {len(audio_segment)} ms\n"
            info += f"channels: {audio_segment.channels}\n"
            info += f"sample_rate: {audio_segment.frame_rate} Hz\n"

            if audio_segment.sample_width > 2:
                print(f"\x1b[2m\x1b[33m    Warning (\"{filename}\"): bit depth > 16 bit may not playback correctly.\x1b[0m")

                # if CLI_ARGS.no_convert_to_s16 is false, auto convert to 16-bit signed integer format for reliability
                if not CLI_ARGS.no_convert_to_s16:
                    audio_segment = audio_segment.set_sample_width(2)
                    print(f"\x1b[2m\x1b[34m    Converting \"{filename}\" to 16-bit signed integer format...\x1b[0m")

            # The server can only reliably play audio at sample rates of 8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000
            # If the sample rate is not in the list, convert to the nearest higher valid sample rate
            valid_sample_rates = [16000, 22050, 32000, 44100, 48000, 88200, 96000, 192000]
            if audio_segment.frame_rate not in valid_sample_rates:
                print(f"\x1b[33m    Warning (\"{filename}\"): Sample rate of {audio_segment.frame_rate} Hz is not supported.\x1b[0m")
                new_sample_rate = min([sr for sr in valid_sample_rates if sr > audio_segment.frame_rate])
                # new_sample_rate = 16000
                print(f"\x1b[34m    --> Resampling \"{filename}\" to {new_sample_rate} Hz sample rate...\x1b[0m")
                
                audio_segment = resample_audio(audio_segment, new_sample_rate)

                info += f"sample_rate_resampled: {audio_segment.frame_rate} Hz\n"

            audio[filename] = {
                "name": filename,
                "filename": f"audio/{filename}",
                "audio": audio_segment,
                "info": info
            }

    print(f"Preloaded {len(audio)} audio files to RAM\n")
    return audio



def make_gapless_playlist(playlist, audio, playlist_name="this playlist"):
    # get the unique steps in the playlist to pre-process the audio files / pauses if necessary
    # filter for unique values in the playlist
    unique_steps = list(set((step["type"], step["value"]) for step in playlist))

    # find the highest sample rate in the audio files, or default to 48000 Hz
    highest_sample_rate = max([audio[step[1]]["audio"].frame_rate for step in unique_steps if step[0] == "audio"], default=48000)

    # print note if all audio files are not at the same sample rate and not at the highest sample rate
    if len(set([audio[step[1]]["audio"].frame_rate for step in unique_steps if step[0] == "audio"])) > 1:
        print(f"\x1b[34m    Note: For \"{playlist_name}\" gapless playback, all audio files will be resampled to {highest_sample_rate} Hz\x1b[0m")

    # Process the audio and pause steps in the playlist
    # processed_audio = {filename: audio_segment, ...}
    # processed_pauses = {duration: audio_segment, ...}
    # This way, even if the same audio file is used multiple times in the playlist, it only needs to be processed once
    processed_audio = {}
    processed_pauses = {}
    for step in unique_steps:
        if step[0] == "audio":
            audio_segment = audio[step[1]]["audio"]

            if audio_segment.frame_rate != highest_sample_rate:
                print(f"\x1b[2m\x1b[34m    --> Resampling \"{step[1]}\" to {highest_sample_rate} Hz sample rate...\x1b[0m")
                audio_segment = resample_audio(audio_segment, highest_sample_rate)

            if audio_segment.channels != 2:
                audio_segment = audio_segment.set_channels(2)

            if audio_segment.sample_width != 2:
                audio_segment = audio_segment.set_sample_width(2)

            # convert the sample to array format
            nparray = audio_segment.get_array_of_samples()

            # add the audio segment to the processed_audio dict
            processed_audio[step[1]] = nparray

        elif step[0] == "pause":
            # create a pause audio segment
            silence =  create_tone(frequency=0, duration=step[1], volume=0, sample_rate=highest_sample_rate, edge=0, channels=2)
            nparray = silence.get_array_of_samples()

            # add the pause audio segment to the processed_pauses dict
            processed_pauses[step[1]] = nparray

        
    # From the processed audio and pause segments, create the collection of numpy arrays for the playlist
    chapters = []
    total_array_length = 0
    nparrays = []
    for step in playlist:
        if step["type"] == "audio":
            nparrays.append(processed_audio[step["value"]])
            total_array_length += len(processed_audio[step["value"]])
            chapters.append([total_array_length / (highest_sample_rate * 2) * 1000, step["value"]])
        elif step["type"] == "pause":
            nparrays.append(processed_pauses[step["value"]])
            total_array_length += len(processed_pauses[step["value"]])
            chapters.append([total_array_length / (highest_sample_rate * 2) * 1000, f"pause_{step['value']}ms"])

    # concatenate the numpy arrays to create the gapless playlist
    gapless_playlist = np.concatenate(nparrays)
    playlistSegment = AudioSegment(gapless_playlist.tobytes(), frame_rate=highest_sample_rate, sample_width=2, channels=2)

    return {
        "segment": playlistSegment,
        "chapters": chapters
    }


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

        gapless_playlist = make_gapless_playlist(playlist, AUDIO, filename)

        playlists[filename] = {
            "name": filename,
            "data": playlist,
            "info": info,
            "gapless": gapless_playlist
        }

    print(f"Loaded {len(playlists)} playlist files\n")
    return playlists



def progress(value, length=40, title="", vmin=0.0, vmax=1.0, postfix="", auto_resize=True):
    """
    Text progress bar.
    
    Parameters
    ----------
    value : float
        Current value to be displayed as progress
    vmin : float
        Minimum value
    vmax : float
        Maximum value
    length: int
        Bar length (in character)
    title: string
        Text to be prepend to the bar
    postfix: string
        Text to be append at the end of the bar
    auto_resize: bool
        Auto adjust bar length to fit the screen size. If False, use the given length
    """
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    # Block progression is 1/8
    blocks = ["", "▏","▎","▍","▌","▋","▊","▉","█"]
    vmin = vmin or 0.0
    vmax = vmax or 1.0
    lsep, rsep = "▏", "▕"

    # if title not end with a whitespace, add one
    if title and not title[-1].isspace(): title += " "
    # if postfix not start with a whitespace, add one
    if postfix and not postfix[0].isspace(): postfix = " " + postfix

    # Auto adjust length to fit the screen by subtracting the length of title, lsep, rsep, percentage (10 char), and postfix
    if auto_resize:
        cols, _ = shutil.get_terminal_size(fallback = (length, 1))
        # limit cols to some % of terminal width
        cols = int(cols * 0.93)
        length = cols - len(title) - len(lsep) - len(rsep) - 10 - len(postfix)

    # Normalize value
    value = min(max(value, vmin), vmax)
    value = (value-vmin)/float(vmax-vmin)
    
    v = value*length
    x = math.floor(v) # integer part
    y = v - x         # fractional part
    base = 0.125      # 0.125 = 1/8
    prec = 3
    i = int(round(base*math.floor(float(y)/base),prec)/base)
    bar = "█"*x + blocks[i]
    n = length-len(bar)
    bar = lsep + bar + " "*n + rsep


    sys.stdout.write(LINE_UP + LINE_CLEAR + title + bar + postfix + " (%.1f%%)" % (value*100) + "\n")
    sys.stdout.flush()


# function progress_timer(time_ms) that uses tqdm to make a timer progress bar
# Usage: playlist_progress_timer(6000, [[0, "First Half"], [2500, "Second Half"]], "Finished!")
def playlist_progress_timer(sink: simpleaudio.PlayObject, total_time_ms, chapters, end_msg="", update_interval_ms=1000, time_stamp_offset=0):
    # sink is the simpleaudio PlayObject

    # chapters is a list of [time_ms (end of chap), description] pairs
    # for example, [[1000, "Chapter 1"], [total_time_ms, "Chapter 2"]]

    # time_stamp_offset is the time when the audio started playing in the past, use it to calculate the actual progress since start
    # if time_stamp_offset is 0, use the current time as the start time
    print("\n")
    if time_stamp_offset == 0:
        time_stamp_offset = time.time_ns() // 1_000_000

    # find the longest chapter description and pad the other with spaces at the start to make them the same length
    max_desc_len = len(max([chapter[1] for chapter in chapters], key=len))
    for i in range(len(chapters)):
        chapters[i][1] = chapters[i][1].rjust(max_desc_len)

    total = total_time_ms // update_interval_ms
    timef_total = time.strftime("%M:%S", time.gmtime(math.ceil(total_time_ms / 1000)))

    desc = chapters[0][1] # default from 0

    # loop start from the (current time - time_stamp_offset)
    loopstart = (time.time_ns() // 1_000_000 - time_stamp_offset) // update_interval_ms

    # there is a chance that loopstart is negative (process took a long time to spawn) --> return with the highest chapter
    if loopstart < 0:
        return len(chapters)

    currentChapter = 0
    # update the actual currentChapter
    for i in range(len(chapters)):
        if chapters[i][0] > loopstart * update_interval_ms:
            currentChapter = i
            break

    def time_to_chap(currentChapter):
        i = (time.time_ns() // 1_000_000 - time_stamp_offset) // update_interval_ms
        for j in range(currentChapter, len(chapters)):
            if chapters[j][0] > i * update_interval_ms:
                return j
        return currentChapter

    # The main loop for updating the progress bar
    for i in range(loopstart, total):        
        # since processing time is not 0, update i to reflect the actual time from time_start_ms
        i = (time.time_ns() // 1_000_000 - time_stamp_offset) // update_interval_ms
        if i > total:
            break

        # update the actual currentChapter based on the current time
        currentChapter = time_to_chap(currentChapter)

        # if the audio has been stopped, break the loop and return
        if sink is None or not sink.is_playing():
            return time_to_chap(currentChapter)
        
        desc = f"[{currentChapter + 1}/{len(chapters)}]  {chapters[currentChapter][1]}"
        # format time as mm:ss playback / mm:ss total
        # [00:05 / 1:00]
        timef = time.strftime("%M:%S", time.gmtime(i * update_interval_ms / 1000))
        timef = f"{timef} / {timef_total}"
        
        progress(i, vmax=total-1, title=desc, postfix=f"[{timef}]")

        # recall this, as things might have changed
        if sink is None or not sink.is_playing():
            return time_to_chap(currentChapter)

        sleep(update_interval_ms / 1000)
    
    if end_msg != "":
        print(end_msg)
    print()

    return len(chapters)


def send_ttl_pulse():
    # send a TTL pulse to the TTL device
    if SERIAL_DEVICE is not None:
        bytes_to_send = bytearray()
        for i in range(PULSE_BYTE_COUNT):
            bytes_to_send.append(0xFF)
        sentlength = SERIAL_DEVICE.write(bytes_to_send)
        print("\x1b[2m\x1b[34m    Sent TTL pulse to the Serial device ({} bytes)\x1b[0m".format(sentlength))
    else:
        print("\x1b[2m\x1b[33m    WARNING: No TTL device found. TTL pulse not sent.\x1b[0m")



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