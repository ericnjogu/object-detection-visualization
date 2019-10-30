import cv2
import numpy
import argparse
import grpc
from concurrent import futures
import tempfile
import logging
import time

import object_detection.utils.label_map_util as label_utils
import object_detection.utils.visualization_utils as vis_utils
from proto.generated import detection_handler_pb2_grpc, detection_handler_pb2


class VideoDetectionHandler(detection_handler_pb2_grpc.DetectionHandlerServicer):
    def __init__(self, path_to_label_map):
        self.category_index = None
        self.output_video_file_path = None
        self.video_writer = None
        self.path_to_label_map = path_to_label_map

    def get_category_index(self):
        if not self.category_index:
            # generate dict from labels
            self.category_index = label_utils.create_category_index_from_labelmap(self.path_to_label_map, use_display_name=True)
        return self.category_index

    def get_output_video_file_path(self):
        if not self.output_video_file_path:
            self.output_video_file_path = tempfile.NamedTemporaryFile(suffix='.avi', delete=False).name
            logging.info(f'writing output video to {self.output_video_file_path}')
        return self.output_video_file_path

    def init_video_writer(self, frame_height, frame_width):
        """ initialize video_writer with the given height, width"""
        return cv2.VideoWriter(self.get_output_video_file_path(),
                                        fourcc=cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                        apiPreference=cv2.CAP_ANY,
                                        fps=10,
                                        frameSize=(int(frame_height), int(frame_width)))

    def handle_detection(self, request, context):
        """
        handle a detection output
        """
        if self.video_writer is None:
          self.video_writer = self.init_video_writer(request.float_map['frame_height'], request.float_map['frame_width'])

        frame = numpy.array(request.frame.numbers).reshape(request.frame.shape)
        boxes = numpy.array(request.detection_boxes.numbers).reshape(request.detection_boxes.shape)
        vis_utils.visualize_boxes_and_labels_on_image_array(
          frame,
          boxes,
          request.detection_classes,
          request.detection_scores,
          self.get_category_index(),
          use_normalized_coordinates=True,
          line_thickness=10)
        output_rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        self.video_writer.write(output_rgb)

        return detection_handler_pb2.handle_detection_response(status=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=" mark detected objects on an image")
    parser.add_argument("path_to_label_map", help="path to label map")
    parser.add_argument("handler_port", help="port to listen for detection handling requests")
    args = parser.parse_args()
    # credit - https://www.semantics3.com/blog/a-simplified-guide-to-grpc-in-python-6c4e25f0c506/
    # create server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # add implementing class to server
    video_handler = VideoDetectionHandler(args)
    detection_handler_pb2_grpc.add_DetectionHandlerServicer_to_server(video_handler, server);
    # listen
    port = args.handler_port
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info(f'starting server on port {port}')
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    # sleep loop
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        video_handler.video_writer.release()
        server.stop(0)
