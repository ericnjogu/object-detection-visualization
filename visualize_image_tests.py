import unittest.mock as mock

import pytest

from visualize_image import VideoDetectionHandler


def test_create_handle_detection_request(create_handle_detection_request):
    """
    Tests that the input data is serialized okay into the protobuf types without errors
    Receives a fixture function defined in proto.conftest.py which is loaded by pytest
    """
    msg, string_map, float_map, category_index = create_handle_detection_request
    handler = VideoDetectionHandler("/test/path/to/labels")
    # mocks
    handler.video_writer = mock.Mock()
    handler.category_index = category_index
    handler.output_video_file_path = mock.Mock()
    # https://medium.com/@yeraydiazdiaz/what-the-mock-cheatsheet-mocking-in-python-6a71db997832
    with mock.patch('visualize_image.cv2') as mocked_cv2:
        handler.handle_detection(msg, mock.Mock())

    # assertions
    handler.video_writer.write.assert_called_once()

# https://www.avivroth.com/2018/03/06/python-embedding-pytest-in-code/
if __name__ == "__main__":
    pytest.main([__file__])
