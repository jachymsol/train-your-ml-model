import cv2

from utils.image_utils import crop_to_square

def create():
    return cv2.VideoCapture(0)

def capture(camera):
    ret, frame = camera.read()
    if not ret: 
        raise EOFError("Failed to get picture from the camera")
    return crop_to_square(frame)

def destroy(camera):
    camera.release()
    cv2.destroyAllWindows()
