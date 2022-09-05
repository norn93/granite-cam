from pathlib import Path

import numpy as np
import cv2
import json
import os

directory_name = "/home/george/Videos/GraniteCam/"

# Set the path to the directory that contains the video files
path = Path(directory_name)

# Print the file names
for file_name in path.rglob('*.AVI'):
    print(file_name)

    # Open the video file
    capture = cv2.VideoCapture(str(file_name))
    cv2.namedWindow("Frame")

    # Do we have a good mask?
    mask_file_name = os.path.splitext(file_name)[0] + ".mask"
    mask_good = None
    try:
        with open(mask_file_name, "r") as f:
            opened_mask = json.loads(f.read())
            mask = np.asarray(opened_mask)
            mask_good = True
    except FileNotFoundError:
        mask = np.array([[0, 0]], ndmin=2)

    # Keeping the last frame
    last_frame = np.array([None])

    # Get all the frames
    while(capture.isOpened()):
        # If the mask is good, or we don't know
        if mask_good == None or mask_good == True:
            # If we don't know, we can asusme it's bad
            if mask_good == None:
                print("No mask found, continuing")
                mask_good = False
            ret, frame = capture.read()

            frame_mask_lines = frame.copy()

        # Converting to gray-scale 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #cv2.polylines(frame_mask_lines, [mask], True, (0,255,0), thickness=3)

        x = gray.shape[0]
        y = gray.shape[1]

        # Get the right part of the image only
        # Blank frame
        image_mask = np.zeros(shape=[x, y], dtype=np.uint8)
        # Fill the area
        cv2.fillPoly(image_mask, [mask], 1)
        # Mask it
        masked_gray_frame = cv2.copyTo(gray, image_mask)

        key = cv2.waitKey(1) & 0xFF

        # For each frame, mask out the right area
        # This differs from video to video, so...
        # if no mask file exists for some video, make one
        # if the 'c' key is pressed, continue, the mask is correct
        if key == ord("c"):
            mask_good = True
        # If 'q' is pressed, quit this video
        elif key == ord("q"):
            break
        # If 'n' is pressed, advance 1 frame
        elif key == ord("n"):
            mask_good = None

        # Keep the last frame
        if last_frame.any() == None:
            last_frame = masked_gray_frame.copy()
            continue

        # Subtract the images
        frame_difference = np.subtract(masked_gray_frame, last_frame)

        print(np.average(np.average(masked_gray_frame)))
        print(np.average(np.average(last_frame)))
        print(np.average(np.average(frame_difference)))


        print(masked_gray_frame.dtype)
        print(last_frame.dtype)
        print(frame_difference.dtype)

        # Show the frame
        cv2.imshow('Frame', last_frame)

        # Find step changes in the change

        # Save the last frame
        last_frame = masked_gray_frame.copy()
    
    # Relinquish the file
    capture.release()

# close all open windows
cv2.destroyAllWindows()