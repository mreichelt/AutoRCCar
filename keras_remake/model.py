from keras import Sequential
from keras.layers import Dense, Flatten, Dropout, Cropping2D, Convolution2D


def drive_model():
    model: Sequential = Sequential([
        # remove top / bottom part of the image, they contain data that is mostly not useful
        Cropping2D(cropping=((110, 0), (0, 0)), input_shape=(240, 320, 1)),

        # convolutional layers + pooling
        Convolution2D(24, 3, 1, activation='relu', subsample=(2, 2)),
        Convolution2D(36, 3, 1, activation='relu', subsample=(2, 2)),
        Convolution2D(48, 3, 1, activation='relu', subsample=(2, 2)),
        # Convolution2D(48, 3, 3, activation='relu', subsample=(2, 2)),
        # Convolution2D(64, 3, 1, activation='relu'),
        # Convolution2D(64, 3, 1, activation='relu'),

        # some fully connected layers, added dropout to reduce overfitting

        Flatten(),
        # Dropout(0.5),
        # Dense(50),
        Dropout(0.5),
        Dense(10),
        Dense(1),
    ])

    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['accuracy'],
    )
    return model


def brake_model():
    model: Sequential = Sequential([
        # no cropping?

        # convolutional layers + pooling
        Convolution2D(24, 3, 3, activation='relu', subsample=(2, 2), input_shape=(240, 320, 1)),
        Convolution2D(36, 3, 3, activation='relu', subsample=(2, 2)),
        Convolution2D(48, 3, 3, activation='relu', subsample=(2, 2)),
        # Convolution2D(64, 3, 1, activation='relu'),
        # Convolution2D(64, 3, 1, activation='relu'),

        # some fully connected layers, added dropout to reduce overfitting

        Flatten(),
        # Dropout(0.5),
        # Dense(50),
        Dropout(0.5),
        Dense(10),
        Dense(1),
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy'],
    )
    return model
