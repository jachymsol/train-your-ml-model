import numpy as np
from PIL import Image, ImageEnhance

def compose(f1, f2):
    return lambda x: f1(f2(x))

def flip(image):
    return image.transpose(Image.FLIP_TOP_BOTTOM)

def to_grayscale(image):
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
    return do_transforms(image_array, flip, to_grayscale, resize, max_contrast)
