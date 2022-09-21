# Graphs the movement for each video
# First, run 'masker.py' to generate masks

from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import csv
import math
import matplotlib.collections as collections

directory_name = "/home/george/Videos/GraniteCam/"

TRUTH_FILENAME = "labels.csv"

# Set the path to the directory that contains the video files
path = Path(directory_name)

# But, only look at the first 75%
file_names = list(path.rglob('*.data'))
n = round(0.75 * len(file_names))
file_names = file_names[:n]

print("Looking at first 75% of files only, which is", n, "files...")

# Print the file names
for file_name in path.rglob('*.data'):
    print(file_name)

    frame = list()
    mog = list()
    shadow = list()

    # Load the data in
    with open(file_name, "r") as f:
        csv_file = csv.DictReader(f, delimiter=',', fieldnames=['frame','mog','shadow'])
        for row in csv_file:
            frame.append(int(row["frame"]))
            mog.append(math.log10(float(row["mog"]) + 0.00001))
            shadow.append(math.log10(float(row["shadow"]) + 0.00001))

    # Load in the truth
    truth = list()
    truth_y = list()
    truth.append(0)
    truth_y.append(-5)
    with open(TRUTH_FILENAME, "r") as f:
        csv_file = csv.DictReader(f, delimiter=",", fieldnames=['Date', 'Granite', 'Northing', 'Easting', 'LS/ BG/ NE', 'Camera', 'Video file name', 'Date', 'Video start', 'Time start', 'Time end', 'Reptiles?', 'Species', 'No. individuals', 'Activity', 'Weather', 'Notes'])
        for row in csv_file:
            if str(row["Video file name"]) == str(file_name).split("/")[-1].split(".")[0]:
                # We did see something in this video
                video_start = row['Video start']
                start = row['Time start']
                end = row['Time end']
                if start == "" or end == "":
                    print("WEATHER/NOTE:", row["Weather"], row["Notes"])
                else:
                    video_start = datetime.strptime(video_start, "%H:%M:%S")
                    start_datetime = datetime.strptime(start, "%H:%M:%S")
                    end_datetime = datetime.strptime(end, "%H:%M:%S")
                    
                    segment_start = start_datetime - video_start
                    segment_end = end_datetime - video_start

                    # In this case, 1 second is 1 frame. So, we now have them
                    # TODO: Generalise for different framerates etc
                    frame_start = segment_start.seconds
                    frame_end = segment_end.seconds

                    truth.append(frame_start)
                    truth.append(frame_end)

                    truth_y.append(-5)
                    truth_y.append(0)

                    
    # Cnvert the data to numpy
    mog = np.asarray(mog)
    shadow = np.asarray(shadow)
    truth = np.asarray(truth)

    # Graph the data
    fig, ax = plt.subplots()
    ax.plot(mog)
    ax.plot(shadow)
    ax.step(truth, truth_y, linewidth=1.0, alpha=0.3)
    plt.show()