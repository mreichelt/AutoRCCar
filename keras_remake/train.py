import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split

from keras_remake.data import load_drive_data, load_brake_data
from keras_remake.model import drive_model, brake_model

drive_model = drive_model()
brake_model = brake_model()


def training_drive():
    features, labels = load_drive_data('labeled_images')

    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.2)

    print(drive_model.summary())
    cvscores = []

    history = drive_model.fit(train_features, train_labels, epochs=20, validation_split=0.2)

    drive_model.save('drive.h5')

    scores = drive_model.evaluate(test_features, test_labels, verbose=1)

    print("%s: %.2f%%" % (drive_model.metrics_names[1], scores[1] * 100))
    cvscores.append(scores[1] * 100)

    print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))
    # save history plot to history.png
    drive_fig = plt.figure('drive')
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model mean squared error loss')
    plt.ylabel('mean squared error loss')
    plt.yscale('log')
    plt.ylim(0, 50)
    plt.xlabel('epoch')
    plt.legend(['training set', 'validation set'], loc='upper right')
    drive_fig.savefig('drive_history.png')
    plt.interactive(True)
    drive_fig.show()
    input()


def training_brake():
    features, labels = load_brake_data('labeled_images')

    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.2,
                                                                                random_state=42)
    print(brake_model.summary())

    history = brake_model.fit(train_features, train_labels, epochs=5, validation_split=0.3)

    brake_model.save('brake.h5')

    drive_fig = plt.figure('brake')
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model mean squared error loss')
    plt.ylabel('mean squared error loss')
    plt.xlabel('epoch')
    plt.legend(['training set', 'validation set'], loc='upper right')
    drive_fig.savefig('brake_history.png')


if __name__ == '__main__':
    training_drive()
    # training_brake()
