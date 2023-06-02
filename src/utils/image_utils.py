import cv2
from pathlib import Path

from utils.config import get_config

def crop_to_square(frame):
    h, w = frame.shape[:2]
    min_dim = min(h, w)
    start_x = (w - min_dim) // 2
    start_y = (h - min_dim) // 2
    return frame[start_y:start_y+min_dim, start_x:start_x+min_dim]

def get_next_image_filename(dataset_path, category):
    folder_path = Path.expanduser(Path(dataset_path) / category)
    current_filenames = [file.name for file in folder_path.glob('im_*.png')]
    current_filenames.sort()
    if len(current_filenames) > 0:
        last_number = int(current_filenames[-1][3:-4])
    else:
        last_number = -1
    new_filename = f"im_{str(last_number+1).zfill(6)}.png"
    return folder_path / new_filename

def save_image(image, image_path):
    cv2.imwrite(str(image_path), cv2.resize(image, (128, 128)))

def delete_image(image_path):
    Path.unlink(Path(image_path))
