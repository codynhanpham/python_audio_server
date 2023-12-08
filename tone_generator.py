# Generate tones specified in a csv file: frequency (Hz), duration (ms), volume (dB), and sample rate (Hz)
# defaults: 440 Hz, 100 ms, 60 dB, 44100 Hz

import os
import csv

import numpy as np
from scipy.io import wavfile

def main():
    output_dir = "tones/"


    # user input for the csv file
    csv_file = input("Enter the csv file path: ")
    # validate csv file
    if not os.path.isfile(csv_file):
        print("Invalid csv file. The program will now restart.")
        return main()
    
    data = []
    # read csv file
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # there should be 4 columns: frequency (Hz), duration (ms), volume (dB), and sample rate (Hz)
        # no header row
        # if column is empty or invalid, use default value

        # default values
        frequency = 440
        duration = 100
        volume = 60
        sample_rate = 44100

        # iterate through each row, validate, and add to data
        for row in reader:
            try:
                frequency = float(row[0])
            except:
                print(f"Row {reader.line_num}: Frequency is invalid. Using default value.")

            try:
                duration = int(row[1])
            except:
                print(f"Row {reader.line_num}: Duration is invalid. Using default value.")

            try:
                volume = float(row[2])
            except:
                print(f"Row {reader.line_num}: Volume is invalid. Using default value.")

            try:
                sample_rate = int(row[3])
            except:
                print(f"Row {reader.line_num}: Sample rate is invalid. Using default value.")

            # add to data
            data.append([frequency, duration, volume, sample_rate])


    # make sure output directory exists
    output_dir = output_dir.rstrip("/")
    output_dir += "/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # create the sine wave
    # iterate through each row in data
    for row in data:
        # unpack the row
        frequency, duration, volume, sample_rate = row
        # calculate the number of samples
        samples = int(sample_rate * duration / 1000)
        # calculate the x values
        x = np.arange(samples)
        # calculate the y values
        y = np.sin(2 * np.pi * frequency * x / sample_rate)
        # scale the y values
        y *= 10 ** (volume / 20)
        # convert to 16-bit data
        y = y.astype(np.int16)
        # save the audio file
        wavfile.write(f"{output_dir}{frequency}Hz_{duration}ms_{volume}dB_@{sample_rate}Hz.wav", sample_rate, y)
        print(f"Saved {frequency}Hz_{duration}ms_{volume}dB_@{sample_rate}Hz.wav")

    print("Done!")


if __name__ == "__main__":
    main()
