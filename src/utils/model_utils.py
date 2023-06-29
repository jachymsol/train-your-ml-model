import numpy as np
import tensorflow as tf
from tensorflow import keras
from pathlib import Path
from sklearn.utils import shuffle

import utils.image_utils as image_utils
from utils.config import get_config
from utils.transformations import max_contrast_for_model

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

def save_model(model, state_folder):
    current_models = sorted(state_folder.glob('model_'))
    file_numbers = [int(filename[-5:]) for filename in current_models]
    if len(file_numbers) > 0:
        last_number = max(file_numbers)
    else:
        last_number = -1

    model_folder = state_folder / f"model_{str(last_number).zfill(5)}"
    Path.mkdir(model_folder)
    model.save(model_folder)
    return Path.absolute(model_folder)

def create_generator(dataset_path, active_upgrades, is_test=False):
    color_mode = 'grayscale' if 'grayscale' in active_upgrades else 'rgb'
    target_size = (32, 32) if 'resize' in active_upgrades else (128, 128)
    preprocessing_function = max_contrast_for_model if 'contrast' in active_upgrades else None
    validation_split = 0.2 if 'train_test_split' in active_upgrades else 0

    if 'image_generation' in active_upgrades:
        datagen = keras.preprocessing.image.ImageDataGenerator(
            rescale=1./255,
            preprocessing_function=preprocessing_function,
            rotation_range=10,
            width_shift_range=0.1,
            height_shift_range=0.1,
            shear_range=0.1,
            zoom_range=0.1,
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

def create_dataset_from_folder(dataset_path, active_upgrades, is_test=False):
    categories = get_config('categories')
    n_cats = range(len(categories))
    filenames = [list((dataset_path / category).glob('*.png')) for category in categories]
    image_arrays = np.array([image_utils.load(str(filename)) for i in n_cats for filename in filenames[i]])
    image_labels = np.concatenate([np.zeros(len(filenames[0])), np.ones(len(filenames[1]))])
    transformed_image_arrays = np.array([image_utils.transform(image, active_upgrades) for image in image_arrays])
    rescaled_image_arrays = 1 - transformed_image_arrays * 1./255
    x, y = shuffle(rescaled_image_arrays, image_labels)
    if 'train_test_split' in active_upgrades:
        offset = int(np.floor(len(x) * 0.8))
        if is_test:
            return x[offset:], y[offset:]
        return x[:offset], y[:offset]
    return x, y

def create_train_and_evaluate(active_upgrades, state_folder):
    model = create_model(active_upgrades)

    train_dataset_path = Path.expanduser(Path(get_config('train_folder')))
    train_x, train_y = create_dataset_from_folder(train_dataset_path, active_upgrades)
    test_x, test_y = [], []

    history = model.fit(train_x, train_y, batch_size=32, epochs=10)
    test_accuracy = history.history['accuracy'][-1]

    if 'train_test_split' in active_upgrades:
        test_x, test_y = create_dataset_from_folder(train_dataset_path, active_upgrades, is_test=True)

        test_results = model.evaluate(test_x, test_y, return_dict=True)
        test_accuracy = test_results['accuracy']

    model_info = {
        'model_path': save_model(model, state_folder),
        'active_upgrades': active_upgrades,
        'samples': f"{len(train_y)} + {len(test_y)}",
        'train_accuracy': test_accuracy,
        'test_accuracy': None
    }
    return model_info

def test(model_path, active_upgrades):
    model = keras.models.load_model(model_path)
    test_dataset_path = Path.expanduser(Path(get_config('test_folder')))
    active_upgrades_no_split = set(active_upgrades)
    active_upgrades_no_split.discard('train_test_split')
    test_x, test_y = create_dataset_from_folder(test_dataset_path, active_upgrades_no_split)

    results = model.evaluate(test_x, test_y, return_dict=True)
    return results['accuracy']
