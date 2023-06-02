import numpy as np
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
