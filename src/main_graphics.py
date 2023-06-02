from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.properties import BooleanProperty, DictProperty
from kivy.config import Config

import utils.camera_utils as camera_utils
import utils.image_utils as image_utils
from utils.config import get_config

Builder.load_file("graphics/frame.kv")
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class TrainingDataTab(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_interval(self.update_file_chooser, 5.0)

    def update_file_chooser(self, _):
        self.ids.file_chooser._update_files()

    def show_selected_image(self):
        if len(self.ids.file_chooser.selection) > 0:
            self.ids.file_image.source = self.ids.file_chooser.selection[0]
        self.ids.delete_image_button.disabled = False

    def delete_selected_image(self):
        image_utils.delete(self.ids.file_image.source)
        self.ids.file_image.source = ''
        self.ids.delete_image_button.disabled = True

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
                      if self.parent_root.ids.show_transformations_switch.active 
                      else [])
        image_utils.transform_and_display(self.image, self.ids.camera_image, transforms)
    
    def capture_image(self):
        self.is_capturing = False

    def retake_image(self):
        self.is_capturing = True
    
    def save_image(self):
        image_path = image_utils.get_file_name(
            get_config('train_folder'),
            get_config('categories')[0] if self.is_selected_first_category else get_config('categories')[1]
        )
        image_utils.save(self.image, image_path)
        self.is_capturing = True

class UpgradesTab(Widget):
    pass

class PurchasableUpgrade(Widget):
    is_purchased = BooleanProperty(False)
    
    def purchase(self):
        self.is_purchased = True
        self.ids.purchase_row.remove_widget(self.ids.purchase_button)
        self.ids.active_switch.active = True
        self.update_active_state()

    def update_active_state(self):
        if self.ids.active_switch.active:
            self.app_root.state['active_upgrades'].add(self.upgrade_id)
        else:
            self.app_root.state['active_upgrades'].discard(self.upgrade_id)

class OneTimeUpgrade(Widget):
    pass

class TrainYourModelGame(Widget):
    state = DictProperty({
        'active_upgrades': set()
    })

class TrainYourModelApp(App):
    def build(self):
        return TrainYourModelGame()

if __name__ == "__main__":
    TrainYourModelApp().run()
