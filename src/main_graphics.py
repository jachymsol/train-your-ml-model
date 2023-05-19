from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.clock import Clock

from utils.upload_utils import *
from utils.config import get_config

Builder.load_file("graphics/frame.kv")

class TrainingDataTab(Widget):
    pass

class UploadPictureFrame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.camera = create_camera()
        self.is_capturing = True
        Clock.schedule_interval(self.update_camera, 1.0 / 30)

    def update_camera(self, dt):
        if self.camera.isOpened() and self.is_capturing:
            image = capture(self.camera)

            # Convert image into Kivy Texture
            buf = cv2.flip(image, 0).tobytes()
            texture = Texture.create(
                size=(image.shape[1], image.shape[0]),
                colorfmt='bgr'
            )
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.camera_image.texture = texture

class TrainYourModelGame(Widget):
    pass

class TrainYourModelApp(App):
    def build(self):
        return TrainYourModelGame()

if __name__ == "__main__":
    TrainYourModelApp().run()
