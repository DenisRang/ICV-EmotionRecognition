import tensorflow as tf
from keras_preprocessing.image import ImageDataGenerator
from tensorflow import keras

from random import uniform
import numpy as np
from tensorflow.keras.initializers import RandomNormal
from tensorflow.python.keras.layers.normalization_v2 import BatchNormalization

from extract_data import load_extended_ck_data
from tensorflow.keras.layers import Conv2D, MaxPooling2D, MaxPool1D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import pandas as pd


print(tf.__version__)
print(keras.__version__)


batch_size = 64
epochs = 100
data_augmentation = True
num_classes = 8

x, y = load_extended_ck_data()
x = np.asarray(x) / 255.0
x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                    test_size=0.1,
                                                    shuffle=False,
                                                    random_state=42)
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train,
                                                    test_size=1/9,
                                                    shuffle=False,
                                                    random_state=42)
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
y_val = keras.utils.to_categorical(y_val, num_classes)

model = keras.models.Sequential()
model.add(BatchNormalization(input_shape=x_train.shape[1:]))
k = uniform(0.2, 1.2)
sigma = k / 96
init = RandomNormal(mean=0.0, stddev=sigma)
model.add(Conv2D(64,
                 (5, 5),
                 padding='same',
                 input_shape=x_train.shape[1:],
                 activation='relu',
                 use_bias=False,
                 kernel_initializer=init))
model.add(MaxPooling2D(pool_size=(2, 2)))
sigma = k / 48
init = RandomNormal(mean=0.0, stddev=sigma)
model.add(Conv2D(128,
                 (5, 5),
                 activation='relu',
                 use_bias=False,
                 kernel_initializer=init))
model.add(MaxPooling2D(pool_size=(2, 2)))
sigma = k / 22
init = RandomNormal(mean=0.0, stddev=sigma)
model.add(Conv2D(256,
                 (5, 5),
                 activation='relu',
                 use_bias=False,
                 kernel_initializer=init))
model.add(MaxPooling2D(pool_size=(2, 2),
                       strides=2))
model.add(Flatten())
model.add(Dense(300))
model.add(Dropout(0.5))
model.add(Dense(num_classes,
                activation='softmax'))
model.summary()

opt = keras.optimizers.SGD(learning_rate=0.01, decay=1e-5, momentum=0.9)
model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

if not data_augmentation:
    print('Not using data augmentation.')
    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_data=(x_val, y_val),
              shuffle=False)
else:
    print('Using real-time data augmentation.')
    datagen = ImageDataGenerator(
        rotation_range=30,
        zoom_range=0.20,
        width_shift_range=0.25,
        height_shift_range=0.25,
        shear_range=0.20,
        horizontal_flip=True,
        fill_mode="nearest")

    # Fit the model on the batches generated by datagen.flow().
    history = model.fit_generator(datagen.flow(x_train, y_train,
                                     batch_size=batch_size),
                        epochs=epochs,
                        validation_data=(x_val, y_val))

scores = model.evaluate(x_test, y_test)
print(scores)



pd.DataFrame(history.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1) # set the vertical range to [0-1]
plt.show()







