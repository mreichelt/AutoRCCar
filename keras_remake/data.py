from glob import glob
from pathlib import Path

import cv2


def load_data(root='labeled_images'):
    images = load_images(root)
    return zip(map(get_prediction_by_name, images), map(load_image_by_name, images))


def get_prediction_by_name(image):
    return float(Path(image).parent.name)


def load_image_by_name(image):
    return cv2.imread(image, cv2.IMREAD_GRAYSCALE)


def load_images(root):
    return glob(root + '/**/*.jpg')
