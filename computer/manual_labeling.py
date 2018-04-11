import sys
import time
from pathlib import Path

import cv2
import numpy as np
import pygame
import glob

NUM_KEYS = [getattr(pygame, 'K_' + str(num)) for num in range(10)]


def main():
    image_array = np.zeros((1, 38400))
    label_array = np.zeros((1, 1), 'float')
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
        label_array = np.vstack((label_array, np.array(label, 'float')))
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
            pressed_nums = list(filter(lambda key: pressed[key], NUM_KEYS))
            if len(pressed_nums) == 1:
                return pressed_nums[0]

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
