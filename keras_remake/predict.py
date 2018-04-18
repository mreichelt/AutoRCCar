import argparse
import sys
from typing import Union, List

import cv2
import h5py
import keras
import numpy as np


def load_image(image: Union[np.ndarray, str]):
    if isinstance(image, str):
        image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    return image


class NeuralNetwork:

    def __init__(self, model_path):
        h5file = h5py.File(model_path, mode='r')
        model_version = h5file.attrs.get('keras_version')
        keras_version = str(keras.__version__).encode('utf8')

        if model_version != keras_version:
            print('Keras version(%s) != model version(%s)' % (keras_version, model_version), file=sys.stderr)

        self.model = keras.models.load_model(model_path)
        print(self.model.summary())

    def predict_single(self, image: Union[str, np.ndarray]):
        return self.predict([load_image(image)])[0]

    def predict(self, images: Union[List[np.ndarray], np.ndarray]):
        if isinstance(images, list):
            images = np.array(images)
        return self.model.predict(images.reshape(images.shape[0], *(self.model.layers[0].input_shape[1:])))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model',
        type=str,
        help='Your model.h5 file'
    )
    parser.add_argument(
        'images',
        nargs='+',
        type=str,
        help='images to find predictions for'
    )
    ns = parser.parse_args()
    model = NeuralNetwork(ns.model)
    for image in ns.images:
        print(image, model.predict_single(image))


if __name__ == '__main__':
    main()
