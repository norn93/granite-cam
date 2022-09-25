# Measures the movement for each video

# If 'Esc' is pressed, quit this video

import numpy as np
import cv2

from pathlib import Path

import numpy as np
import cv2
import json
import os
from time import sleep

directory_name = "/home/george/Videos/GraniteCam/"

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

# Set the path to the directory that contains the video files
path = Path(directory_name)

fourcc = cv2.VideoWriter_fourcc(*"MJPG")

# Print the file names
for file_name in path.rglob('*.mov'):
    print(file_name)
    if "20210824 1533 Gull Rock Timelapse Camera 3" not in str(file_name):
    # if "20210920 Waychinicup Camera1 14.00 to 16.23.mov" not in str(file_name):
        continue

    data_file_name = os.path.splitext(file_name)[0] + ".data"

    # Open the video file
    capture = cv2.VideoCapture(str(file_name))

    # Get the output ready for writing
    out = cv2.VideoWriter(os.path.splitext(file_name)[0] + '_output.avi', fourcc, 10.0, (720, 405+405))

    # background_subtraction_method = cv2.createBackgroundSubtractorMOG2(detectShadows=False, history=0, backgroundRatio=0.2)
    background_subtraction_method1 = cv2.createBackgroundSubtractorMOG2(history=0, varThreshold=0, detectShadows=False)
    background_subtraction_method2 = cv2.createBackgroundSubtractorKNN(history=0, dist2Threshold=1000, detectShadows=False)

    count = 0

    while capture.isOpened():
        
        ret, frame = capture.read()
        if not ret:
            break
        count += 1
        # if count < 970:
        #     continue

        # Converting to gray-scale 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        fgmask1 = background_subtraction_method1.apply(gray)
        # fgmask2 = background_subtraction_method2.apply(gray)

        # fgmask1 = cv2.morphologyEx(fgmask1, cv2.MORPH_OPEN, kernel)

        # concatenate image Horizontally
        # Hori = np.concatenate((img1, img2), axis=1)

        # Resize images
        # gray_small = cv2.resize(gray, (720, 405))
        frame_small = cv2.resize(frame, (720, 405))
        fgmask1_small = cv2.resize(fgmask1, (720, 405))

        # Make it 'colour'
        fgmask1_small_colour = cv2.cvtColor(fgmask1_small, cv2.COLOR_GRAY2RGB)

        
        # concatenate image Vertically
        images = np.concatenate((frame_small, fgmask1_small_colour), axis=0)

        cv2.imshow('Frame', images)

        out.write(images)

        # If 'Esc' is pressed, quit this video
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    capture.release()
    cv2.destroyAllWindows()