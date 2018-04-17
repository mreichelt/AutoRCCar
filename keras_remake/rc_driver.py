from array_util import find_subarray_np
from keras_remake.predict import NeuralNetwork
from random_util import get_my_ip
from serial_util import select_car

__author__ = 'zhengwang'

import socketserver
import cv2
import cv2.ml
import numpy as np

sensor_data = []

STEER_THRESHOLD = 0.3
GAS_INTERVAL = 3


class RCControl(object):

    def __init__(self):
        self.car = select_car()
        self.car.start()

    def steer(self, prediction, frame):
        print(end=str(frame))
        if prediction < -STEER_THRESHOLD:
            if frame % GAS_INTERVAL != 0:
                print('left')
                self.car.left()
            else:
                print('forward left')
                self.car.forward_left()
        elif prediction > STEER_THRESHOLD:
            if frame % GAS_INTERVAL != 0:
                print('right')
                self.car.right()
            else:
                print('forward right')
                self.car.forward_right()
        else:
            if frame % GAS_INTERVAL != 0:
                self.car.reset_car()
                print("stop")
            else:
                self.car.forward()
                print("Forward")

    def stop(self):
        self.car.reset_car()


class SensorDataHandler(socketserver.BaseRequestHandler):
    data = " "

    def handle(self):
        global sensor_data
        try:
            while self.data:
                self.data = self.request.recv(1024)
                sensor_data = round(float(self.data), 1)
                # print "{} sent:".format(self.client_address[0])
                print(sensor_data)
        finally:
            print("Connection closed on thread 2")


JPEG_START = np.array([0xff, 0xd8], dtype=np.uint8)
JPED_END = np.array([0xff, 0xd9], dtype=np.uint8)


class VideoStreamHandler(socketserver.StreamRequestHandler):
    # create neural network
    model = NeuralNetwork('models/default.h5')

    rc_car = RCControl()

    def handle(self):

        global sensor_data
        stream_bytes = np.array([], dtype=np.uint8)

        # stream video frames one by one
        try:
            frame = 0
            first = None
            while True:
                stream_bytes = np.append(stream_bytes, np.fromstring(self.rfile.read(8 * 1024), dtype=np.uint8))
                if first is None:
                    first = find_subarray_np(stream_bytes, JPEG_START)
                if first is not None:
                    last = find_subarray_np(stream_bytes, JPED_END)
                    if last is not None:
                        jpg = stream_bytes[first:last + 2]
                        stream_bytes = stream_bytes[last + 2:]
                        gray = cv2.imdecode(jpg, cv2.IMREAD_GRAYSCALE)

                        prediction = self.model.predict_single(gray)

                        self.rc_car.steer(prediction, frame)

                        frame += 1

                        first = None

        finally:
            self.rc_car.stop()
            cv2.destroyAllWindows()
            print("Connection closed on thread 1")


class ThreadServer(object):

    @staticmethod
    def server_thread(host, port):
        server = socketserver.TCPServer((host, port), VideoStreamHandler)
        server.serve_forever()

    def __init__(self):
        ThreadServer.server_thread('0.0.0.0', 8000)


if __name__ == '__main__':
    print(get_my_ip())
    ThreadServer()
