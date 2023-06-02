import tensorflow as tf
from tensorflow import keras
import numpy as np
from pathlib import Path
from PIL import Image

from utils.config import get_config
from utils.transformations import full_transform

def train_dataset():
    train_dataset = Path.expanduser(Path(get_config('train_folder')))
    # test_dataset = Path.expanduser(Path(get_config['test_folder']))

    datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    preprocessing_datagen = keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        preprocessing_function=full_transform
    )
    enhanced_datagen = keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    train_generator = preprocessing_datagen.flow_from_directory(
        train_dataset,
        target_size=(128, 128),
        batch_size=32,
        class_mode='categorical'
    )

    # test_generator = datagen.flow_from_directory(
    #     test_dataset,
    #     target_size=(224, 224),
    #     batch_size=32,
    #     class_mode='categorical'
    # )

    model = keras.Sequential([
        keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(256, 256, 3)),
        keras.layers.MaxPooling2D((2,2)),
        keras.layers.Conv2D(64, (3,3), activation='relu'),
        keras.layers.MaxPooling2D((2,2)),
        keras.layers.Conv2D(64, (3,3), activation='relu'),
        keras.layers.Flatten(),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(2)
    ])

    model.compile(
        optimizer=keras.optimizers.legacy.Adam(0.001),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )

    model.fit(train_generator, epochs=10)

    # model.evaluate(test_generator, verbose=2)