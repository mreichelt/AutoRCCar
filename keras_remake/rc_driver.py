from array_util import find_subarray_np
from keras_remake.predict import NeuralNetwork
from random_util import get_my_ip
from serial_util import select_car

__author__ = 'zhengwang'

import threading
import socketserver
import cv2
import cv2.ml
import numpy as np
import atexit

sensor_data = None

STEER_THRESHOLD = 0.3
GAS_INTERVAL = 3


class RCControl(object):

    def __init__(self):
        self.car = select_car()
        self.car.start()
        self.last_distance = 3000

    def steer(self, prediction, frame, distance):
        print(end="%05d: " % frame)

        if self.last_distance >= 25 > distance:
            self.car.horn()
        self.last_distance = distance

        if distance < 20:
            print('stop, because of obstacle')
            self.car.reset_car()
            return

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
                print('Got sensor data:', sensor_data)
        finally:
            print("Connection closed on thread 2")


JPEG_START = np.array([0xff, 0xd8], dtype=np.uint8)
JPED_END = np.array([0xff, 0xd9], dtype=np.uint8)


class VideoStreamHandler(socketserver.StreamRequestHandler):

    def __init__(self, request, client_address, server):
        self.rc_car = RCControl()
        atexit.register(self.rc_car.stop)
        self.model = NeuralNetwork('models/default.h5')
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
                    last = find_subarray_np(stream_bytes, JPED_END)
                    if last is not None:
                        jpg = stream_bytes[first:last + 2]
                        stream_bytes = stream_bytes[last + 2:]
                        gray = cv2.imdecode(jpg, cv2.IMREAD_GRAYSCALE)

                        self.model.predict([cv2.imread("training_images/frame01094.jpg", cv2.IMREAD_GRAYSCALE)])

                        prediction = (max(min(self.model.predict_single(gray), 9), 1) - 5) / 4

                        self.rc_car.steer(prediction, frame=frame,
                                          distance=sensor_data if sensor_data is not None else 3000)

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
