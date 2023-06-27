from kivy.properties import BooleanProperty
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget

import utils.camera_utils as camera_utils
import utils.image_utils as image_utils
from utils.config import get_config

Builder.load_file("graphics/training_frame.kv")

class TrainingDataTab(Widget):
    def update_file_chooser(self, _):
        self.ids.file_chooser.update_file_chooser(None)

class UploadImageFrame(Widget):
    is_capturing = BooleanProperty(True)
    is_selected_first_category = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.camera = camera_utils.create()
        Clock.schedule_interval(self.update_camera, 1.0 / 30)

    def update_camera(self, _):
        if self.camera.isOpened() and self.is_capturing:
            self.image = camera_utils.capture(self.camera)
        
        transforms = (self.app_root.state['active_upgrades'] 
                      if self.app_root.state['show_transformations']
                      else [])
        image_utils.transform_and_display(self.image, self.ids.camera_image, transforms)
    
    def capture_image(self):
        self.is_capturing = False

    def retake_image(self):
        self.is_capturing = True
    
    def save_image(self):
        image_path = image_utils.get_next_filename(
            get_config('train_folder'),
            get_config('categories')[0] if self.is_selected_first_category else get_config('categories')[1]
        )
        image_utils.save(self.image, image_path)
        Clock.schedule_once(self.parent_root.update_file_chooser)
        self.app_root.add_coins(1)
        self.is_capturing = True

class FileChooserFrame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_interval(self.update_selected_image, 1./10)
    
    def update_file_chooser(self, _):
        self.ids.file_chooser._update_files()

    def update_selected_image(self, _):
        if len(self.ids.file_chooser.selection) > 0:
            image = image_utils.load(self.ids.file_chooser.selection[0])
            transforms = (self.app_root.state['active_upgrades'] 
                        if self.app_root.state['show_transformations']
                        else [])
            image_utils.transform_and_display(image, self.ids.file_image, transforms)
        self.ids.delete_image_button.disabled = False

    def delete_selected_image(self):
        image_utils.delete(self.ids.file_chooser.selection[0])
        Clock.schedule_once(self.update_file_chooser)
        self.ids.file_chooser.selection = []
        self.ids.file_image.texture = None
        self.ids.delete_image_button.disabled = True
