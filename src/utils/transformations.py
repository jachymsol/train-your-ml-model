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

def smart_contrast(image_array):
    hist, _ = np.histogram(image_array, bins=257, range=(-1, 255))
    peaks, _ = find_peaks(hist, height=15, width=3, distance=20)

    threshold = np.mean(peaks)
    return np.vectorize(lambda x: 255 if x > threshold else 0)(image_array)

def add_dimension(image_array):
    image_array_as_float = np.array(image_array).astype('float32')
    return np.expand_dims(image_array_as_float, -1)

def do_transforms(image_array, *transforms):
    image = Image.fromarray(image_array)
    for transform in transforms:
        image = transform(image)
    return np.array(image)

def full_transform(image_array):
    return do_transforms(image_array, flip, grayscale, resize, max_contrast)

Transformations = {
    "flip": flip,
    "grayscale": grayscale,
    "contrast": max_contrast,
    "resize": resize
}
