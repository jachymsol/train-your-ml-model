import tensorflow as tf
from tensorflow import keras
from pathlib import Path
from PIL import Image

from utils.config import get_config

def create_model():
    model = keras.Sequential([
        keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(128, 128, 1)),
        keras.layers.MaxPooling2D((2,2)),
        keras.layers.Conv2D(64, (3,3), activation='relu'),
        keras.layers.MaxPooling2D((2,2)),
        keras.layers.Conv2D(64, (3,3), activation='relu'),
        keras.layers.Flatten(),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer=keras.optimizers.legacy.Adam(0.001),
        loss=tf.keras.losses.BinaryCrossentropy(),
        metrics=['accuracy']
    )

    return model

def create_generator(preprocessing_fn=None):
    datagen = keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        preprocessing_function=preprocessing_fn
    )

    return datagen.flow_from_directory(
        Path.expanduser(Path(get_config('train_folder'))),
        target_size=(128, 128),
        batch_size=32,
        class_mode='binary',
        color_mode='grayscale'
    )

def train(model, data_generator):
    model.fit(data_generator, epochs=10)

def evaluate(model):
    test_folder = get_config('test_folder')
    model.evaluate(test_folder)
