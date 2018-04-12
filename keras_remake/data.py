from glob import glob
from pathlib import Path

import cv2
import numpy as np


def load_data(root='labeled_images'):
    images = load_images(root)
    return (np.array([load_image_by_name(image).reshape(240, 320, 1) for image in images], 'float'),
            np.array([get_prediction_by_name(image) for image in images]))


def get_prediction_by_name(image):
    return float(Path(image).parent.name)


def load_image_by_name(image):
    return cv2.imread(image, cv2.IMREAD_GRAYSCALE)


def load_images(root):
    return glob(root + '/**/*.jpg')
