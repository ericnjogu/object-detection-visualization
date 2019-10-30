# Detection Visualization
This projects uses the tensorflow object detection utilities to draw bounding boxes, detection scores and object labels on a frame.

The result of each Visualization are then saved as a part of a sequence of images in an output folder.

It implements a service that consumes detection output from https://github.com/kunadawa/video-object-detection via grpc.

## Setup
- download or clone this repo
- Download or clone the [tensorflow models repo](https://github.com/tensorflow/models)
- Download or clone the [video object detection repo](https://github.com/kunadawa/video-object-detection)
- In this repo's root, make the following soft links so that the visualization utils imports can work
 - `[tensorflow-models-root]/research/object_detection`
 - `[video object detection repo]/proto`
- add `[video object detection repo]/proto/generated` to PYTHONPATH

## Running
- `python visualize_image.py object_detection/data/mscoco_complete_label_map.pbtxt 50001`
 
 Replace the label map path as appropriate
## Tests
`visualize_image_tests.py` uses a shared fixture defined in `[video object detection repo]/samples/conftest.py`.
Create a symlink to that file to the root directory then run `pytest visualize_image_tests.py`
