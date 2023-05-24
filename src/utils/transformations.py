import numpy as np
from PIL import Image, ImageEnhance

def compose(f1, f2):
    return lambda x: f1(f2(x))

def flip(image_array):
    image = Image.fromarray(image_array)
    flipped = image.transpose(Image.FLIP_TOP_BOTTOM)
    return np.array(flipped)

def to_grayscale(image_array):
    image = Image.fromarray(image_array)
    grayscale = image.convert('L')
    return np.array(grayscale)

def max_contrast(image_array):
    image = Image.fromarray(image_array)
    enhancer = ImageEnhance.Contrast(image)
    enhanced_im = enhancer.enhance(50)
    return np.array(enhanced_im)

def resize(image_array):
    image = Image.fromarray(image_array)
    resized_im = image.resize((32, 32))
    return np.array(resized_im)

def full_transform(image_array):
    return compose(compose(max_contrast, resize), compose(to_grayscale, flip))(image_array)
