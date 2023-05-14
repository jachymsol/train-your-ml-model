import tensorflow as tf
from tensorflow import keras
import numpy as np
from pathlib import Path
from PIL import Image

def train_dataset(config):
    train_dataset = Path.expanduser(Path(config['train_folder']))
    test_dataset = Path.expanduser(Path(config['test_folder']))

    datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    preprocessing_datagen = keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        preprocessing_function=config['preprocessing']
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

    train_generator = datagen.flow_from_directory(
        train_dataset,
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical'
    )

    test_generator = datagen.flow_from_directory(
        test_dataset,
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical'
    )

    model = keras.Sequential([
        keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(128, 128, 3)),
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

    model.evaluate(test_generator, verbose=2)