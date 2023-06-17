import tensorflow as tf
from tensorflow import keras
from pathlib import Path
from PIL import Image

from utils.config import get_config
from utils.transformations import smart_contrast

def create_model(active_upgrades):
    size = 32 if 'resize' in active_upgrades else 128
    channels = 1 if 'grayscale' in active_upgrades else 3
    input_shape = (size, size, channels)

    model = keras.Sequential([
        keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=input_shape),
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

def create_generator(dataset_path, active_upgrades):
    color_mode = 'grayscale' if 'grayscale' in active_upgrades else 'rgb'
    target_size = (32, 32) if 'resize' in active_upgrades else (128, 128)
    preprocessing_function = smart_contrast if 'contrast' in active_upgrades else None

    datagen = keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        preprocessing_function=preprocessing_function
    )

    return datagen.flow_from_directory(
        dataset_path,
        target_size=target_size,
        batch_size=32,
        class_mode='binary',
        color_mode=color_mode
    )

def create_train_and_evaluate(active_upgrades):
    model = create_model(active_upgrades)
    train_dataset_path = Path.expanduser(Path(get_config('train_folder')))
    train_generator = create_generator(train_dataset_path, active_upgrades)
    model.fit(train_generator, epochs=10)

    test_dataset_path = Path.expanduser(Path(get_config('test_folder')))
    test_generator = create_generator(test_dataset_path, active_upgrades)
    test_results = model.evaluate(test_generator, return_dict=True)

    model_info = {
        'model': model,
        'samples': train_generator.samples,
        'accuracy': test_results['accuracy']
    }
    return model_info