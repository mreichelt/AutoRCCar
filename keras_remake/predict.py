import argparse
import sys
from typing import Union, List

import cv2
import h5py
import keras
import numpy as np

debug = False


class NeuralNetwork:
    def __init__(self, drive, brake=None):
        drive_h5 = h5py.File(drive, mode='r')
        drive_version = drive_h5.attrs.get('keras_version')
        keras_version = str(keras.__version__).encode('utf8')

        if drive_version != keras_version:
            print('Keras version(%s) != drive model version(%s)' % (keras_version, drive_version), file=sys.stderr)

        self.drive_model = keras.models.load_model(drive)

        if brake is not None:
            brake_h5 = h5py.File(brake, mode='r')
            brake_version = brake_h5.attrs.get('keras_version')
            if brake_version != keras_version:
                print('Keras version(%s) != brake model version(%s)' % (keras_version, brake_version), file=sys.stderr)
            self.brake_model = keras.models.load_model(brake)

    def predict_single_drive(self, image: Union[str, np.ndarray]):
        if isinstance(image, str):
            image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        prediction = self.predict([image.reshape(240, 320, 1)])[0]
        return prediction

    def predict_single_brake(self, image: Union[str, np.ndarray]):
        if isinstance(image, str):
            image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        return self.predict_brake([image.reshape(240, 320, 1)])[0]

    def predict_brake(self, images: Union[List[np.ndarray], np.ndarray]):
        if isinstance(images, list):
            images = np.array(images)
        return self.drive_model.predict(images.reshape(images.shape[0], 240, 320, 1))

    def predict(self, images: Union[List[np.ndarray], np.ndarray]):
        if isinstance(images, list):
            images = np.array(images)
        return list(map(lambda out: self.map_output(out[0]),
                        self.drive_model.predict(images.reshape(images.shape[0], 240, 320, 1))))

    @staticmethod
    def map_output(prediction):
        return (max(min(prediction, 9), 1) - 5) / 4


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--drive',
        type=str,
        help='Your drive model.h5 file'
    )
    parser.add_argument(
        '--brake',
        type=str,
        help='Your brake model.h5 file'
    )
    parser.add_argument(
        'images',
        nargs='+',
        type=str,
        help='images to find predictions for'
    )
    ns = parser.parse_args()
    model = NeuralNetwork(ns.drive, ns.brake)
    for image in ns.images:
        print(image, model.predict_single_drive(image), model.predict_single_brake(image))


if __name__ == '__main__':
    main()
