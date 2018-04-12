import keras

from keras_remake.model import model
from keras_remake.data import load_data

import matplotlib

matplotlib.use('agg')

import matplotlib.pyplot as plt

features, labels = load_data('labeled_images')

model = model()

print(model.summary())

history = model.fit(features, labels, epochs=5, validation_split=0.2)

model.save('model.h5')

# save history plot to history.png
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model mean squared error loss')
plt.ylabel('mean squared error loss')
plt.xlabel('epoch')
plt.legend(['training set', 'validation set'], loc='upper right')
plt.savefig('history.png')

if __name__ == '__main__':
    pass
