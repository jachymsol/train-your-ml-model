import tensorflow as tf
from tensorflow import keras
from pathlib import Path
from PIL import Image

from utils.config import get_config
from utils.transformations import smart_contrast_for_model

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

def create_generator(dataset_path, active_upgrades, is_test=False):
    color_mode = 'grayscale' if 'grayscale' in active_upgrades else 'rgb'
    target_size = (32, 32) if 'resize' in active_upgrades else (128, 128)
    preprocessing_function = smart_contrast_for_model if 'contrast' in active_upgrades else None
    validation_split = 0.2 if 'train_test_split' in active_upgrades else 0

    if 'image_generation' in active_upgrades:
        datagen = keras.preprocessing.image.ImageDataGenerator(
            rescale=1./255,
            preprocessing_function=preprocessing_function,
            rotation_range=20,
            width_shift_range=0.1,
            height_shift_range=0.1,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            validation_split=validation_split
        )
    else:
        datagen = keras.preprocessing.image.ImageDataGenerator(
            rescale=1./255,
            preprocessing_function=preprocessing_function,
            validation_split=validation_split
        )

    if is_test:
        return datagen.flow_from_directory(
            dataset_path,
            target_size=target_size,
            batch_size=32,
            class_mode='binary',
            color_mode=color_mode,
            subset='validation'
        )
        
    return datagen.flow_from_directory(
        dataset_path,
        target_size=target_size,
        batch_size=32,
        class_mode='binary',
        color_mode=color_mode,
        subset='training'
    )

def create_train_and_evaluate(active_upgrades):
    model = create_model(active_upgrades)
    train_dataset_path = Path.expanduser(Path(get_config('train_folder')))
    train_generator = create_generator(train_dataset_path, active_upgrades)
    test_generator = create_generator(train_dataset_path, active_upgrades, is_test=True)
    history = model.fit(train_generator, epochs=10)
    test_accuracy = history.history['accuracy'][-1]

    if 'train_test_split' in active_upgrades:
        test_results = model.evaluate(test_generator, return_dict=True)
        test_accuracy = test_results['accuracy']

    model_info = {
        'model': model,
        'active_upgrades': active_upgrades,
        'samples': f"{train_generator.samples} + {test_generator.samples}",
        'train_accuracy': test_accuracy,
        'test_accuracy': None
    }
    return model_info

def test(model, active_upgrades):
    test_dataset_path = Path.expanduser(Path(get_config('test_folder')))
    test_generator = create_generator(test_dataset_path, active_upgrades)

    results = model.evaluate(test_generator, return_dict=True)
    return results['accuracy']
