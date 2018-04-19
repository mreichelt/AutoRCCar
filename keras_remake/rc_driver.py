from multiprocessing import Value

from array_util import find_subarray_np
from keras_remake.predict import NeuralNetwork
from random_util import get_my_ip
from serial_util import select_car, Throttle, Direction

__author__ = 'zhengwang'

import threading
import socketserver
import cv2
import cv2.ml
import numpy as np
import atexit

sensor_data = Value('f', 3000)

STEER_THRESHOLD = 0.3
GAS_INTERVAL = 2
GAS_INTERVAL_LENGTH = 3


class RCControl(object):

    def __init__(self):
        self.car = select_car()
        self.car.start()
        self.last_distance = 3000

    def steer(self, prediction, frame, distance):
        print(end="%05d: " % frame)

        car = self.car

        # honk if too close
        if self.object_is_getting_close(distance):
            car.horn()

        if self.is_obstacle_too_close(distance):
            print('stop, because of obstacle')
            car.reset_car()
            return

        direction = self.convert_to_direction(prediction)
        throttle = self.compute_throttle(frame)

        # car.steer(RIGHT, FORWARD)
        print(throttle.name, '\t', direction.name)
        car.steer(direction, throttle)

    def stop(self):
        self.car.reset_car()

    def object_is_getting_close(self, distance):
        is_getting_closer = self.last_distance > 30 and self.is_obstacle_too_close(distance)
        self.last_distance = distance
        return is_getting_closer

    @staticmethod
    def is_obstacle_too_close(distance):
        return distance <= 30

    @staticmethod
    def convert_to_direction(prediction):
        return Direction.RIGHT if prediction > STEER_THRESHOLD else (Direction.LEFT if prediction < -STEER_THRESHOLD
                                                                     else Direction.STRAIGHT)

    @staticmethod
    def compute_throttle(frame, gas_interval_length=GAS_INTERVAL_LENGTH, gas_interval=GAS_INTERVAL):
        return Throttle.STOP if frame // gas_interval_length % gas_interval != 0 else Throttle.FORWARD


class SensorDataHandler(socketserver.BaseRequestHandler):
    data = " "

    def handle(self):
        global sensor_data
        try:
            while self.data:
                self.data = self.request.recv(1024)
                try:
                    value = round(float(self.data), 1)
                    sensor_data.value = value
                    # print "{} sent:".format(self.client_address[0])
                    print('Got sensor data:', value)
                except ValueError:
                    print('Got sensor data too fast')
        finally:
            print("Connection closed on thread 2")


JPEG_START = np.array([0xff, 0xd8], dtype=np.uint8)
JPEG_END = np.array([0xff, 0xd9], dtype=np.uint8)


class VideoStreamHandler(socketserver.StreamRequestHandler):

    def __init__(self, request, client_address, server):
        self.rc_car = RCControl()
        atexit.register(self.rc_car.stop)
        self.model = NeuralNetwork('models/default.h5',
                                   output_mapping=lambda prediction: (max(min(prediction, 9), 1) - 5) / 4)
        super().__init__(request, client_address, server)

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
                    last = find_subarray_np(stream_bytes, JPEG_END)
                    if last is not None:
                        jpg = stream_bytes[first:last + 2]
                        stream_bytes = stream_bytes[last + 2:]
                        gray = cv2.imdecode(jpg, cv2.IMREAD_GRAYSCALE)

                        prediction = self.model.predict_single(gray)

                        self.rc_car.steer(prediction, frame=frame,
                                          distance=sensor_data.value)

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

    @staticmethod
    def sensor_thread(host, port):
        server = socketserver.TCPServer((host, port), SensorDataHandler)
        server.serve_forever()

    def __init__(self):
        server_thread = threading.Thread(target=ThreadServer.server_thread, args=('0.0.0.0', 8000))
        sensor_thread = threading.Thread(target=ThreadServer.sensor_thread, args=('0.0.0.0', 8002))
        server_thread.start()
        sensor_thread.start()
        server_thread.join()
        sensor_thread.join()


if __name__ == '__main__':
    print(get_my_ip())
    ThreadServer()
