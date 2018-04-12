from array_util import find_subarray
from serial_util import select_car

__author__ = 'zhengwang'

import socketserver
import cv2
import cv2.ml
import numpy as np

sensor_data = []


class NeuralNetwork(object):

    def __init__(self):
        self.model = cv2.ml.ANN_MLP_load('mlp_xml/mlp.xml')

    def create(self):
        pass

    def predict(self, samples):
        ret, resp = self.model.predict(samples)
        return resp.argmax(-1)


class RCControl(object):

    def __init__(self):
        self.car = select_car()

    def steer(self, prediction):
        if prediction == 2:
            self.car.forward()
            print("Forward")
        elif prediction == 0:
            self.car.forward_left()
            print("Left")
        elif prediction == 1:
            self.car.forward_right()
            print("Right")
        else:
            self.stop()

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


class VideoStreamHandler(socketserver.StreamRequestHandler):
    # create neural network
    model = NeuralNetwork()
    model.create()

    rc_car = RCControl()

    def handle(self):

        global sensor_data
        stream_bytes = []

        # stream video frames one by one
        try:
            while True:
                stream_bytes += self.rfile.read(1024)
                first = find_subarray(stream_bytes, [0xff, 0xd8])
                last = find_subarray(stream_bytes, [0xff, 0xd9])
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    gray = cv2.imdecode(np.array(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    image = cv2.imdecode(np.array(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    # lower half of the image
                    half_gray = gray[120:240, :]

                    cv2.imshow('image', image)
                    # cv2.imshow('mlp_image', half_gray)

                    # reshape image
                    image_array = half_gray.reshape(1, 38400).astype(np.float32)

                    # neural network makes prediction
                    prediction = self.model.predict(image_array)

                    # stop conditions
                    self.rc_car.steer(prediction)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.rc_car.stop()
                        break

            cv2.destroyAllWindows()

        finally:
            print("Connection closed on thread 1")


class ThreadServer(object):

    @staticmethod
    def server_thread(host, port):
        server = socketserver.TCPServer((host, port), VideoStreamHandler)
        server.serve_forever()

    def __init__(self):
        ThreadServer.server_thread('0.0.0.0', 8000)


if __name__ == '__main__':
    ThreadServer()
