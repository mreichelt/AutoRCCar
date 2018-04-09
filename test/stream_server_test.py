#!/usr/bin/env python3
from array_util import find_subarray

__author__ = 'zhengwang'

import numpy as np
import cv2
import socket




class VideoStreamingTest(object):
    def __init__(self):

        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 8000))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')
        self.streaming()

    def streaming(self):

        try:
            print("Connection from: ", self.client_address)
            print("Streaming...")
            print("Press 'q' to exit")

            stream_bytes = []
            while True:
                stream_bytes += self.connection.read(1024)
                first = find_subarray(stream_bytes, [0xff, 0xd8])
                last = find_subarray(stream_bytes, [0xff, 0xd9])
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.array(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    print(image.shape)
                    cv2.imshow('image', image)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    VideoStreamingTest()
