import sys
import time
from pathlib import Path

import cv2
import numpy as np
import pygame
import glob


def main():
    image_array = np.zeros((1, 38400))
    label_array = np.zeros((1, 4), 'float')
    identity = np.zeros((4, 4), 'float')
    for i in range(4):
        identity[i, i] = 1
    pygame.init()
    for image in glob.glob('training_images/*.jpg'):
        image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        try:
            label = label_image(image)
        except KeyboardInterrupt:
            break
        if label < 0:
            continue
        roi = image[120:240, :]
        temp_array = roi.reshape(1, 38400).astype(np.float32)
        image_array = np.vstack((image_array, temp_array))
        label_array = np.vstack((label_array, identity[label]))
    save(Path('training_data'), image_array, label_array)
    cv2.destroyAllWindows()
    cv2.waitKey(0)


def save(path, images, labels):
    path.mkdir(parents=True, exist_ok=True)
    path = path / (str(int(time.time())) + '.npz')
    np.savez(str(path), train=images[1:, :], train_labels=labels[1:, :])


def await_key():
    while True:
        for event in pygame.event.get(pygame.KEYDOWN):
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                return 0
            if pressed[pygame.K_UP]:
                return 2
            if pressed[pygame.K_RIGHT]:
                return 1
            if pressed[pygame.K_DOWN]:
                return 3
            if pressed[pygame.K_s]:
                return -1
            if pressed[pygame.K_ESCAPE] or pressed[pygame.K_x] or pressed[pygame.K_q]:
                raise KeyboardInterrupt


def label_image(image):
    cv2.imshow('to-label', image)
    key = await_key()
    return key


if __name__ == '__main__':
    main()
