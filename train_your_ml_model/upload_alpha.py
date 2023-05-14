import cv2
import time
from pathlib import Path

from .upload_utils import *

def upload(config):
    camera = create_camera()
    countdown_3_secs()
    image = capture(camera)
    release_camera(camera)
    print("Image captured successfully")
    category = get_category_name(config["categories"])
    image_path = get_image_file_name(config["train_folder"], category)
    save_image(image, image_path)
    print("Image saved successfully")
