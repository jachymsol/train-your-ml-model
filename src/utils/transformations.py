import numpy as np
from scipy.optimize import curve_fit
from PIL import Image

def gauss(x, mu, sigma, A):
    return A*np.exp(-(x-mu)**2/2/sigma**2)

def flip(image):
    return image.transpose(Image.FLIP_TOP_BOTTOM)

def grayscale(image):
    return image.convert('L')

def max_contrast(image):
    return image.point(lambda x: 0 if x < 128 else 255)

def resize(image):
    return image.resize((32, 32))

def smart_contrast(image):
    image_array = np.array(image)
    hist, _ = np.histogram(image_array, bins=257, range=(-1, 255))
    
    params, _ = curve_fit(gauss, range(120), hist[:120], (90, 10, 100))
    min_cutoff = max(params[0] - 3 * abs(params[1]), 20)
    max_cutoff = min(params[0] + 3 * abs(params[1]), 125)

    return image.point(lambda x: 0 if min_cutoff < x and x < max_cutoff else 255)

def as_float_array(image):
    return np.array(image).astype('float32')

def smart_contrast_for_model(image_array):
    image_size = image_array.shape[0]
    old_image = Image.fromarray(image_array.reshape(image_size, image_size), mode='L')
    new_image = max_contrast(old_image)
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
    "contrast": max_contrast,
    "resize": resize
}
