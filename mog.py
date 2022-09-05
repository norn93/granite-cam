import numpy as np
import cv2

from pathlib import Path

import numpy as np
import cv2
import json
import os

directory_name = "/home/george/Videos/GraniteCam/"

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

# Set the path to the directory that contains the video files
path = Path(directory_name)

# Print the file names
for file_name in path.rglob('*.mov'):
    print(file_name)

    data_file_name = os.path.splitext(file_name)[0] + ".data"

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

    # Open the video file
    capture = cv2.VideoCapture(str(file_name))

    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True)

    count = 0

    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            print(count, "Perhaps an issue?")
            break

        # Converting to gray-scale 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        x = gray.shape[0]
        y = gray.shape[1]

        # Get the right part of the image only
        # Blank frame
        image_mask = np.zeros(shape=[x, y], dtype=np.uint8)
        # Fill the area
        cv2.fillPoly(image_mask, [mask], 1)
        # Mask it
        masked_gray_frame = cv2.copyTo(gray, image_mask)

        fgmask = fgbg.apply(masked_gray_frame)

        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

        # Graphing stuff
        mog = np.average(np.average(fgmask == 255))
        shadow = np.average(np.average(fgmask == 127))
        data = ", ".join([str(count), str(mog), str(shadow)]) + "\n"
        with open(data_file_name, "a+") as f:
            f.write(data)

        #cv2.imshow('Frame', fgmask)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    
        count += 1

    capture.release()
    cv2.destroyAllWindows()