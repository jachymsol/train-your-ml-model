import cv2
import random
from pathlib import Path
from kivy.graphics.texture import Texture

from utils.transformations import add_dimension, do_transforms, smart_contrast, Transformations
from utils.config import get_config

def crop_to_square(image):
    h, w = image.shape[:2]
    min_dim = min(h, w)
    start_x = (w - min_dim) // 2
    start_y = (h - min_dim) // 2
    return image[start_y:start_y+min_dim, start_x:start_x+min_dim]

def transform(image, transforms):
    transformations = [Transformations['flip']]
    if 'grayscale' in transforms:
        transformations.append(Transformations['grayscale'])
    if 'resize' in transforms:
        transformations.append(Transformations['resize'])
    if 'contrast' in transforms:
        transformations.append(Transformations['contrast'])
    return do_transforms(image, *transformations)

def convert_to_kivy_texture(image, colored=True):
    color_fmt = 'bgr' if colored else 'luminance'

    buf = image.tobytes()
    texture = Texture.create(
        size=(image.shape[1], image.shape[0]),
        colorfmt=color_fmt,
    )
    texture.blit_buffer(buf, colorfmt=color_fmt, bufferfmt='ubyte')
    return texture

def transform_and_display(image, canvas, transforms):
    display_image = transform(image, transforms)

    texture = convert_to_kivy_texture(display_image, 'grayscale' not in transforms)
    canvas.texture = texture

def get_next_filename(dataset_path, category):
    folder_path = Path.expanduser(Path(dataset_path) / category)
    current_filenames = [file.name for file in folder_path.glob('train_*.png')]
    current_filenames.sort()
    if len(current_filenames) > 0:
        last_number = int(current_filenames[-1][3:-4])
    else:
        last_number = -1
    new_filename = f"train_{str(last_number+1).zfill(5)}.png"
    return folder_path / new_filename

def load(image_path):
    return cv2.imread(image_path)

def save(image, image_path):
    cv2.imwrite(str(image_path), cv2.resize(image, (128, 128)))

def delete(image_path_string):
    image_path = Path(image_path_string)
    image_name = image_path.parts[-1]
    category = image_path.parts[-2]
    new_path = image_path.parent.parent.parent / 'deleted' / category / image_name
    image_path.rename(new_path)

def copy(src_path, dst_path):
    dst_path.write_bytes(src_path.read_bytes())

def get_random_image_path(dataset):
    dataset_path = Path.expanduser(Path(get_config(f'{dataset}_folder')))
    image_paths = list((dataset_path).rglob(f'{dataset}_*.png'))
    return random.choice(image_paths)

def test_to_train():
    src_path = get_random_image_path('test')
    image_name = src_path.name
    category = src_path.parent.name
    dst_path = src_path.parent.parent.parent / 'train' / category / image_name
    
    copy(src_path, dst_path)

def train_to_test():
    src_path = get_random_image_path('train')
    image_name = src_path.name
    category = src_path.parent.name
    dst_path = src_path.parent.parent.parent / 'test' / category / image_name

    copy(src_path, dst_path)
