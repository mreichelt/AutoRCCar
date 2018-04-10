#!/usr/bin/env python3
from serial_util import select_car

__author__ = 'zhengwang'

import pygame
from pygame.locals import *


class RCTest(object):

    def __init__(self):
        self.car = select_car()
        self.send_inst = True
        pygame.init()
        print("Control with WASD = combinations")
        self.steer()

    def steer(self):

        while self.send_inst:
            for event in pygame.event.get():
                print(event)
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()

                    # complex orders
                    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        print("Forward Right")
                        self.car.forward_right()

                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        print("Forward Left")
                        self.car.forward_left()

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                        print("Reverse Right")
                        self.car.reverse_right()

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                        print("Reverse Left")
                        self.car.reverse_left()

                    # simple orders
                    elif key_input[pygame.K_UP]:
                        print("Forward")
                        self.car.forward()

                    elif key_input[pygame.K_DOWN]:
                        print("Reverse")
                        self.car.reverse()

                    elif key_input[pygame.K_RIGHT]:
                        print("Right")
                        self.car.right()

                    elif key_input[pygame.K_LEFT]:
                        print("Left")
                        self.car.left()

                    # exit
                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print("Exit")
                        self.send_inst = False
                        self.car.reset_car()
                        self.car.close()
                        break

                elif event.type == pygame.KEYUP:
                    self.car.reset_car()


if __name__ == '__main__':
    RCTest()
