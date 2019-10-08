# Detection Visualization
This projects uses the tensorflow object detection utilities to draw bounding boxes, detection scores and object labels on a frame.

The result of each Visualization are then saved as a part of a sequence of images in an output folder.

It a implements a service that consumes detection output from https://github.com/kunadawa/video-object-detection via grpc.

## Setup
- download or clone this repo
- Download or clone the [tensorflow models repo](https://github.com/tensorflow/models)
- In this repo's root, make a soft link to `[tensorflow-models-root]/research/object_detection` so that the visualization utils imports can work
