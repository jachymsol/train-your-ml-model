import numpy as np
from PIL import Image, ImageEnhance

def compose(f1, f2):
    return lambda x: f1(f2(x))

def to_grayscale(image_array):
    image = Image.fromarray(image_array)
    grayscale = image.convert('L')
    return np.array(grayscale)

def max_contrast(image_array):
    image = Image.fromarray(image_array)
    enhancer = ImageEnhance.Contrast(image)
    enhanced_im = enhancer.enhance(50)
    return np.array(enhanced_im)