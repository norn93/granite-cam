# Creates masks for the videos
# For each video in the folder 'directory_name':

# if the 'c' key is pressed, continue, the mask is correct
# If 'm' is pressed, then we need to mask this frame
# If 'q' is pressed, quit this video
# If 'n' is pressed, advance 1 frame
# If 's' is pressed, save the mask
# If 'd' is pressed, delete the mask

from pathlib import Path

import numpy as np
import cv2
import json
import os

directory_name = "/home/george/Videos/GraniteCam/"

print("Starting GraniteCam V1.0...")
print("Processing", directory_name, "...")

def crop(event, x, y, flags, param):
    global mask
    global frame, frame_mask_lines
    if event == cv2.EVENT_LBUTTONDOWN:
        if np.array_equal(mask, np.array([[0, 0]])):
            mask = np.array([[x, y]])
        else:
            mask = np.append(mask, [[x, y]], axis=0)
        frame_mask_lines = frame.copy()


# Set the path to the directory that contains the video files
path = Path(directory_name)

# Print the file names
for file_name in path.rglob('*.mov'):
    print(file_name)

    # Open the video file
    capture = cv2.VideoCapture(str(file_name))
    cv2.namedWindow("Frame")
    cv2.setMouseCallback("Frame", crop)

    # Do we have a good mask?
    mask_file_name = os.path.splitext(file_name)[0] + ".mask"
    try:
        with open(mask_file_name, "r") as f:
            opened_mask = json.loads(f.read())
            mask = np.asarray(opened_mask)
    except FileNotFoundError:
        mask = np.array([[0, 0]], ndmin=2)
    mask_good = None

    # Get all the frames
    while(capture.isOpened()):
        # If the mask is good, or we don't know
        if mask_good == None or mask_good == True:
            # If we don't know, we can asusme it's bad
            if mask_good == None:
                mask_good = False
            ret, frame = capture.read()

            frame_mask_lines = frame.copy()

        cv2.polylines(frame_mask_lines, [mask], True, (0,255,0), thickness=3)
    
        # Show the frame
        cv2.imshow('Frame', frame_mask_lines)

        key = cv2.waitKey(1) & 0xFF

        # For each frame, mask out the right area
        # This differs from video to video, so...
        # if no mask file exists for some video, make one
        # if the 'c' key is pressed, continue, the mask is correct
        if key == ord("c"):
            mask_good = True
        # If 'm' is pressed, then we need to mask this frame
        elif key == ord("m"):
            mask_good = False
        # If 'q' is pressed, quit this video
        elif key == ord("q"):
            break
        # If 'n' is pressed, advance 1 frame
        elif key == ord("n"):
            mask_good = None
        # If 's' is pressed, save the mask
        elif key == ord("s"):
            plain_mask = []
            for line in mask:
                new_coord = []
                for coord in line:
                    new_coord.append(int(coord))
                plain_mask.append(list(new_coord))
            dump = json.dumps(plain_mask)
            
            with open(mask_file_name, "w+") as f:
                f.write(dump)
        # If 'd' is pressed, delete the mask
        elif key == ord("d"):
            mask = np.array([[0, 0]], ndmin=2)

        # Make a histogram of the image in each axis

        # Find step changes in the histograms (???)
    
    # Relinquish the file
    capture.release()

# close all open windows
cv2.destroyAllWindows()