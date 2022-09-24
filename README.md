# Lizard monitoring - GraniteCam

## Situation

* Thousands of hours of timelapse video of granite outcrops, with sparse lizard actvity
* Objective: detect all of the lizards

## Plan

1. Tune the BGS model to produce useful looking output from the labelled videos in the training set
![Input](./media/input.png)
![BGS](./media/bgs.png)
2. Draw bounding boxes around each frame for each lizard
![Bounding box](./media/bound.jpg)
3. Mask the BGS output with these bounding boxes, forming the required output of the training set with the RGB video as the input
![Output](./media/output.jpg)
4. Increase the size of the training set by augmenting using salt and pepper, cropping and resizing, flipping through the y axis, etc.
![Salt and Pepper](./media/salt.jpg)
![Cropping and resizing](./media/crop.jpg)
![Flipping](./media/flip.jpg)
5. Train a CNN on the training set
![Input](./media/input.png)
![Output](./media/output.jpg)
6. Validate on the validation set

## TODO
* Insert an image for each step of the plan
* Link this to Ashwin