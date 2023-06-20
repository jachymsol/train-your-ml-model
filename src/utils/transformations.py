import numpy as np
from scipy.signal import find_peaks
from PIL import Image, ImageEnhance

def flip(image):
    return image.transpose(Image.FLIP_TOP_BOTTOM)

def grayscale(image):
    return image.convert('L')

def max_contrast(image):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(50)

def resize(image):
    return image.resize((32, 32))

def smart_contrast(image):
    image_array = np.array(image)
    hist, _ = np.histogram(image_array, bins=257, range=(-1, 255))
    peaks, _ = find_peaks(hist, height=15, width=3, distance=20)

    threshold = np.mean(peaks)
    return image.point(lambda x: 255 if x > threshold else 0)

def as_float_array(image):
    return np.array(image).astype('float32')

def smart_contrast_for_model(image_array):
    image_size = image_array.shape[0]
    old_image = Image.fromarray(image_array.reshape(image_size, image_size), mode='L')
    new_image = smart_contrast(old_image)
    return add_dimension(as_float_array(new_image))

def add_dimension(image_array):
    return np.expand_dims(as_float_array(image_array), -1)

def do_transforms(image_array, *transforms):
    image = Image.fromarray(image_array)
    for transform in transforms:
        image = transform(image)
    return np.array(image)

def full_transform(image_array):
    return do_transforms(image_array, flip, grayscale, resize, smart_contrast)

Transformations = {
    "flip": flip,
    "grayscale": grayscale,
    "contrast": smart_contrast,
    "resize": resize
}
