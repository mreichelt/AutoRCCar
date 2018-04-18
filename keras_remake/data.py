from glob import glob
from pathlib import Path

import cv2
import numpy as np


def load_drive_data(root='labeled_images'):
    images = load_drive_images(root)
    return (np.array([load_image_by_name(image).reshape(240, 320, 1) for image in images], 'float'),
            np.array([get_prediction_by_name(image) for image in images]))


def load_brake_data(root='labeled_images'):
    brake_images = load_brake_images(root)
    drive_images = load_drive_images(root)
    return (
        np.array([load_image_by_name(image).reshape(240, 320, 1) for image in brake_images]
                 + [load_image_by_name(image).reshape(240, 320, 1) for image in drive_images], 'float'),
        np.append(np.repeat(1, len(brake_images)),
                  np.repeat(0, len(drive_images)))
    )


def get_prediction_by_name(image):
    return float(Path(image).parent.name)


def load_image_by_name(image):
    return cv2.imread(image, cv2.IMREAD_GRAYSCALE)


def load_brake_images(root):
    return [name for name in load_all_images(root) if 'brake' in name]


def load_drive_images(root):
    return [name for name in load_all_images(root) if 'brake' not in name]


def load_all_images(root):
    return filter(lambda name: 'skip' not in name, glob(root + '/**/*.jpg'))
