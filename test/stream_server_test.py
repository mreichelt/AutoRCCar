#!/usr/bin/env python3
from pathlib import Path

from array_util import find_subarray_np
from random_util import get_my_ip

__author__ = 'zhengwang'

import numpy as np
import cv2
import socket

JPEG_START = np.array([0xff, 0xd8], dtype=np.uint8)
JPEG_END = np.array([0xff, 0xd9], dtype=np.uint8)


class VideoStreamingTest(object):
    def __init__(self):

        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 8000))
        self.server_socket.listen(0)
        print("Listening on port 8000. My IP is " + get_my_ip())
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')
        self.streaming()

    def streaming(self):
        try:
            print("Connection from: ", self.client_address)
            print("Streaming...")
            print("Press 'q' to exit")

            Path('training_images').mkdir(parents=True, exist_ok=True)

            stream_bytes = np.array([], dtype=np.uint8)
            frame = 0
            first = None
            while True:
                stream_bytes = np.append(stream_bytes, np.fromstring(self.connection.read(8 * 1024), dtype=np.uint8))
                if first is None:
                    first = find_subarray_np(stream_bytes, JPEG_START)
                if first is not None:
                    last = find_subarray_np(stream_bytes, JPEG_END)
                    if last is not None:
                        jpg = stream_bytes[first:last + 2]
                        stream_bytes = stream_bytes[last + 2:]
                        image = cv2.imdecode(jpg, cv2.IMREAD_GRAYSCALE)
                        cv2.imshow('image', image)
                        print("Frame: %d" % frame)
                        cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)
                        frame += 1
                        first = None
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    VideoStreamingTest()
