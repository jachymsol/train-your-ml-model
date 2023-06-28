import numpy as np
from scipy.optimize import curve_fit
from PIL import Image

# Conversions
def rgb_to_bgr(image_array):
    return image_array[:, :, ::-1]

def as_image(image_array, mode='RGB'):
    return Image.fromarray(rgb_to_bgr(image_array), mode)

def as_array(image):
    return np.array(rgb_to_bgr(image)).copy()

def as_float_array(image):
    return np.array(rgb_to_bgr(image)).astype('float32').copy()

def add_dimension(image_array):
    return np.expand_dims(as_float_array(image_array), -1)

# Transformations
def flip(image):
    return image.transpose(Image.FLIP_TOP_BOTTOM)

def grayscale(image):
    return image.convert('L')

def max_contrast(image):
    return image.point(lambda x: 0 if x < 128 else 255)

def resize(image):
    return image.resize((32, 32))

def max_contrast_for_model(image_array):
    image_size = image_array.shape[0]
    old_image = as_image(image_array.reshape(image_size, image_size), mode='L')
    new_image = max_contrast(old_image)
    return add_dimension(as_float_array(new_image))

# Composing
def do_transforms(image_array, *transforms):
    image = as_image(image_array)
    for transform in transforms:
        image = transform(image)
    return as_array(image)

Transformations = {
    "flip": flip,
    "grayscale": grayscale,
    "contrast": max_contrast,
    "resize": resize
}
