import cv2
import time
from pathlib import Path

def create_camera():
    return cv2.VideoCapture(0)

def capture(camera):
    ret, frame = camera.read()
    if not ret: 
        raise EOFError("Failed to get picture from the camera")
    return crop_frame_to_square(frame)

def release_camera(camera):
    camera.release()
    cv2.destroyAllWindows()

def crop_frame_to_square(frame):
    h, w = frame.shape[:2]
    min_dim = min(h, w)
    start_x = (w - min_dim) // 2
    start_y = (h - min_dim) // 2
    return frame[start_y:start_y+min_dim, start_x:start_x+min_dim]

def get_category_name(avaliable_categories):
    while True:
        category = input("Enter the category of this image: ")
        if category in avaliable_categories:
            return category
        print("This category is not available. Please choose another one.")

def get_image_file_name(dataset_path, category):
    folder_path = Path.expanduser(Path(dataset_path) / category)
    files = [file.name for file in folder_path.glob('im_*.png')]
    files.sort()
    if len(files) > 0:
        last_number = int(files[-1][3:-4])
    else:
        last_number = -1
    image_name = f"im_{str(last_number+1).zfill(6)}.png"
    return folder_path / image_name

def save_image(image, image_path):
    cv2.imwrite(str(image_path), cv2.resize(image, (128, 128)))

def remove_last_image(config):
    category = get_category_name(config["categories"])
    folder_path = Path.expanduser(Path(config["train_folder"]) / category)
    files = [file.name for file in folder_path.glob('im_*.png')]
    files.sort()
    Path.unlink(folder_path / files[-1])

def countdown_3_secs():
    print("Taking picture in 3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)