# Can annotate a file if you want to do it by hand. Creates a '.truth' file.

from pathlib import Path

import numpy as np
import cv2
import json
import os

def label(event, x, y, flags, param):
    global signal
    if event == cv2.EVENT_LBUTTONDOWN:
        signal = 1
    if event == cv2.EVENT_LBUTTONUP:
        signal = 0

directory_name = "/home/george/Videos/GraniteCam/"

print("Starting GraniteCam V1.0...")
print("Processing", directory_name, "...")

# Set the path to the directory that contains the video files
path = Path(directory_name)

# Print the file names
for file_name in path.rglob('*.mp4'):
    print(file_name)

    truth_file_name = os.path.splitext(file_name)[0] + ".truth"

    # Open the video file
    capture = cv2.VideoCapture(str(file_name))
    cv2.namedWindow("Frame")
    cv2.setMouseCallback("Frame", label)

    count = 0
    signal = 0

    # Get all the frames
    while(capture.isOpened()):
        ret, frame = capture.read()

        # Show the frame
        cv2.imshow('Frame', frame)

        key = cv2.waitKey(1) & 0xFF

        print("Frame:", count, signal)
        data = ", ".join([str(count), str(signal)])

        with open(truth_file_name, "a+") as f:
            f.write(data)

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