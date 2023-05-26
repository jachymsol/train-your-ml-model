from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.properties import BooleanProperty
from kivy.config import Config

from utils.upload_utils import *
from utils.transformations import *
from utils.config import get_config

Builder.load_file("graphics/frame.kv")
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class TrainingDataTab(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_interval(self.update_file_chooser, 1.0)

    def update_file_chooser(self, _):
        self.ids.file_chooser._update_files()

    def show_selected_image(self):
        if len(self.ids.file_chooser.selection) > 0:
            self.ids.file_image.source = self.ids.file_chooser.selection[0]
        self.ids.delete_image_button.disabled = False

    def delete_selected_image(self):
        remove_image(self.ids.file_image.source)
        self.ids.file_image.source = ''
        self.ids.delete_image_button.disabled = True

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
        if self.parent_root.ids.show_transformations_switch.active:
            display_image = full_transform(self.image)
            color_fmt = 'luminance'
        else: 
            display_image = do_transforms(self.image, flip)
            color_fmt = 'bgr'
        buf = display_image.tobytes()
        texture = Texture.create(
            size=(display_image.shape[1], display_image.shape[0]),
            colorfmt=color_fmt,
        )
        texture.blit_buffer(buf, colorfmt=color_fmt, bufferfmt='ubyte')
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

class UpgradesTab(Widget):
    pass

class PurchasableUpgrade(Widget):
    pass

class TrainYourModelGame(Widget):
    pass

class TrainYourModelApp(App):
    def build(self):
        return TrainYourModelGame()

if __name__ == "__main__":
    TrainYourModelApp().run()
