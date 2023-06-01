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
    return image.resize((128, 128))

def do_transforms(image_array, *transforms):
    image = Image.fromarray(image_array)
    for transform in transforms:
        image = transform(image)
    return np.array(image)

Transformations = {
    "flip": flip,
    "to_grayscale": to_grayscale,
    "max_contrast": max_contrast,
    "resize": resize
}

def transform_with(image_array, transformations_array):
    transforms = [Transformations[t] for t in transformations_array]
    return do_transforms(image_array, *transforms)

def resize_transform(image_array):
    return do_transforms(image_array, flip, resize)

def full_transform(image_array):
    return do_transforms(image_array, flip, to_grayscale, resize, max_contrast)

def smart_transform(image_array, store):
    transformations = [flip]
    print(store.exists('resize'))
    if store.exists('to_grayscale') and store.get('to_grayscale'):
        transformations.append(to_grayscale)
    if store.exists('resize') and store.get('resize'):
        transformations.append(resize)
    if store.exists('max_contrast') and store.get('max_contrast'):
        transformations.append(max_contrast)
    return do_transforms(image_array, *transformations)
