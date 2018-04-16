import argparse
import sys
import time
from typing import Union, List

import cv2
import h5py
import keras
import numpy as np

debug = False


class NeuralNetwork:
    def __init__(self, model):
        f = h5py.File(model, mode='r')
        model_version = f.attrs.get('keras_version')
        keras_version = str(keras.__version__).encode('utf8')

        if model_version != keras_version:
            print('Keras version(%s) != model version(%s)' % (keras_version, model_version), file=sys.stderr)

        self.model = keras.models.load_model(model)

    def predict_single(self, image: Union[str, np.ndarray]):
        if isinstance(image, str):
            image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        start = time.time()
        prediction = self.predict([image.reshape(240, 320, 1)])[0]
        return prediction

    def predict(self, images: Union[List[np.ndarray], np.ndarray]):
        if isinstance(images, list):
            images = np.array(images)
        return list(map(lambda out: self.map_output(out[0]),
                        self.model.predict(images.reshape(images.shape[0], 240, 320, 1))))

    @staticmethod
    def map_output(prediction):
        return (max(min(prediction, 9), 1) - 5) / 4


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
