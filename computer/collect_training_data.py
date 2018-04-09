from serial_util import select_usbmodem
from array_util import find_subarray

__author__ = 'zhengwang'

import numpy as np
import cv2
import serial
import pygame
from pygame.locals import *
import socket
import time
import os


def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


COLOR_DIMENSIONS = 3


class CollectTrainingData(object):

    def __init__(self):

        # connect to a seral port
        # '/dev/tty.usbmodem1421'
        self.ser = serial.Serial(select_usbmodem(), 115200, timeout=1)
        self.send_inst = True

        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 8000))
        self.server_socket.listen(0)

        print('Waiting for incoming connection. My ip is: ' + get_my_ip())

        # accept a single connection
        self.connection = self.server_socket.accept()[0].makefile('rb')

        # create labels
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 4), 'float')

        pygame.init()
        self.collect_image()

    def collect_image(self):

        saved_frame = 0
        total_frame = 0

        # collect images for training
        print('Start collecting images...')
        e1 = cv2.getTickCount()
        image_array = np.zeros((1, 38400, COLOR_DIMENSIONS))
        label_array = np.zeros((1, 4), 'float')

        # stream video frames one by one
        try:
            stream_bytes = []
            frame = 1
            while self.send_inst:
                stream_bytes += self.connection.read(1024)
                first = find_subarray(stream_bytes, [0xff, 0xd8])
                last = find_subarray(stream_bytes, [0xff, 0xd9])
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.array(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    # select lower half of the image
                    roi = image[120:240, :]

                    # save streamed images
                    cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)

                    # cv2.imshow('roi_image', roi)
                    cv2.imshow('image', image)

                    # reshape the roi image into one row array
                    temp_array = roi.reshape(1, 38400, COLOR_DIMENSIONS).astype(np.float32)

                    frame += 1
                    total_frame += 1

                    # get input from human driver
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            key_input = pygame.key.get_pressed()

                            # complex orders
                            if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                                print("Forward Right")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                saved_frame += 1
                                self.ser.write(bytes([6]))

                            elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                                print("Forward Left")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                self.ser.write(bytes([7]))

                            elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                                print("Reverse Right")
                                self.ser.write(bytes([8]))

                            elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                                print("Reverse Left")
                                self.ser.write(bytes([9]))

                            # simple orders
                            elif key_input[pygame.K_UP]:
                                print("Forward")
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[2]))
                                self.ser.write(bytes([1]))

                            elif key_input[pygame.K_DOWN]:
                                print("Reverse")
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[3]))
                                self.ser.write(bytes([2]))

                            elif key_input[pygame.K_RIGHT]:
                                print("Right")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                saved_frame += 1
                                self.ser.write(bytes([3]))

                            elif key_input[pygame.K_LEFT]:
                                print("Left")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                self.ser.write(bytes([4]))

                            elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                                print('exit')
                                self.send_inst = False
                                self.ser.write(bytes([0]))
                                break

                        elif event.type == pygame.KEYUP:
                            self.ser.write(bytes([0]))

            # save training images and labels
            train = image_array[1:, :]
            train_labels = label_array[1:, :]

            # save training data as a numpy file
            file_name = str(int(time.time()))
            directory = "training_data"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                np.savez(directory + '/' + file_name + '.npz', train=train, train_labels=train_labels)
            except IOError as e:
                print(e)

            e2 = cv2.getTickCount()
            # calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print('Streaming duration:', time0)

            print(train.shape)
            print(train_labels.shape)
            print('Total frame:', total_frame)
            print('Saved frame:', saved_frame)
            print('Dropped frame', total_frame - saved_frame)

        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    CollectTrainingData()
