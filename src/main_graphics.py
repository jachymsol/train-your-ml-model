from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty
from kivy.config import Config

from utils.upload_utils import *
from utils.config import get_config

Builder.load_file("graphics/frame.kv")
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class TrainingDataTab(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_interval(self.update_file_chooser, 1.0)

    def update_file_chooser(self, _):
        self.ids.file_chooser._update_files()

    def show_selected_file(self):
        if len(self.ids.file_chooser.selection) > 0:
            self.ids.file_image.source = self.ids.file_chooser.selection[0]

class UploadPictureFrame(Widget):
    is_capturing = BooleanProperty(True)
    is_selected_first_category = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.camera = create_camera()
        Clock.schedule_interval(self.update_camera, 1.0 / 30)

    def update_camera(self, _):
        if self.camera.isOpened() and self.is_capturing:
            self.image = capture(self.camera)
            self.update_camera_image()

    def update_camera_image(self):
        # Convert image into Kivy Texture
        buf = cv2.flip(self.image, 0).tobytes()
        texture = Texture.create(
            size=(self.image.shape[1], self.image.shape[0]),
            colorfmt='bgr'
        )
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.ids.camera_image.texture = texture
    
    def capture_image(self):
        self.is_capturing = False

    def retake_image(self):
        self.is_capturing = True
    
    def save_image(self):
        image_path = get_image_file_name(
            get_config('train_folder'),
            'airplane' if self.is_selected_first_category else 'basketball'
        )
        save_image(self.image, image_path)
        self.is_capturing = True

class TrainYourModelGame(Widget):
    pass

class TrainYourModelApp(App):
    def build(self):
        return TrainYourModelGame()

if __name__ == "__main__":
    TrainYourModelApp().run()
