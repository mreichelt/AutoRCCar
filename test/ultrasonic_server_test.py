from random_util import get_my_ip

__author__ = 'zhengwang'

import socket
import time


class SensorStreamingTest(object):
    def __init__(self):

        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 8002))
        print("I am listening on ip, port: ", get_my_ip(), 8002)
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.streaming()

    def streaming(self):

        try:
            print("Connection from: ", self.client_address)
            start = time.time()

            while True:
                sensor_data = float(self.connection.recv(1024))
                print("Distance: %0.1f cm" % sensor_data)

                # testing for 10 seconds
                if time.time() - start > 10:
                    pass  # break
        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    SensorStreamingTest()
