# View when the data suggests that the lizards are present, according to the MOG algorithm

# If 'q' is pressed, quit this video

from pathlib import Path

import numpy as np
import cv2
import json
import os

import math

directory_name = "/home/george/Videos/GraniteCam/"

print("Starting GraniteCam V1.0...")
print("Processing", directory_name, "...")

# Set the path to the directory that contains the video files
path = Path(directory_name)

# Print the file names
for file_name in path.rglob('*.mov'):
    print(file_name)

    data_file_name = os.path.splitext(file_name)[0] + ".data"

    f = open(data_file_name, "r")

    # Open the video file
    capture = cv2.VideoCapture(str(file_name))
    cv2.namedWindow("Frame")
    # cv2.setMouseCallback("Frame", label)

    count = 0

    # Get all the frames
    while(capture.isOpened()):
        ret, frame = capture.read()

        data = f.readline().split(",")

        try:
            signal1 = float(data[1].strip())
            signal2 = float(data[2].strip())
        except IndexError:
            print("File complete")
            break

        if signal1 > 0:
            cv2.circle(frame, (50,50), 3*min(100, max(0, int(math.log(1/signal1)))), (0,255,0), -1)
        if signal2 > 0:
            cv2.circle(frame, (150,50), 3*min(100, max(0, int(math.log(1/signal2)))), (0,0,255), -1)
        if signal1 > 10**-4:# and signal2 > 3*10**-4:
            cv2.circle(frame, (250,50), 50, (255,0,0), -1)

        # Show the frame
        cv2.imshow('Frame', frame)

        key = cv2.waitKey(1) & 0xFF

        print("Frame:", count, signal1, signal2)

        # For each frame, mask out the right area
        # This differs from video to video, so...
        # if no mask file exists for some video, make one
        # If 'q' is pressed, quit this video
        if key == ord("q"):
            break

        # Make a histogram of the image in each axis

        # Find step changes in the histograms (???)

        count += 1
    
    # Relinquish the file
    capture.release()

# close all open windows
cv2.destroyAllWindows()