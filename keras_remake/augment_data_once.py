from pathlib import Path

import numpy as np
import cv2

from keras_remake.data import load_drive_images

if __name__ == '__main__':
    files = load_drive_images('labeled_images')
    images = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in files]
    flipped_images = [np.fliplr(image) for image in images]
    labels = [int(Path(file).parent.name) for file in files]
    flipped_labels = [10 - label for label in labels]

    for label, file, image in zip(flipped_labels, files, flipped_images):
        new_path = 'labeled_images/%d/flipped_%s' % (label, Path(file).name)
        print("%s -> flip -> %s" % (file, new_path))
        cv2.imwrite(new_path, image)
