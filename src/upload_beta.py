from kivy.app import App
from kivy.graphics.texture import Texture
from kivy.properties import DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
import cv2

from upload_utils import *
from config import *

class UploadBox(BoxLayout):
    def __init__(self, **kwargs):
        super(UploadBox, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Create a widget to display the camera output
        self.img = Image()
        self.add_widget(self.img)

        # Create a dropdown to choose the category
        self.category = Spinner(
            text=get_config["categories"][0],
            values=get_config["categories"]
        )
        self.add_widget(self.category)

        # Create a button to take a picture
        self.button = Button(text='Take Picture', size_hint=(1, 0.2))
        self.button.bind(on_press=self.on_button_press)
        self.add_widget(self.button)

        # Initialize the camera
        self.capture = create_camera()
        self.is_capturing = True
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        if self.is_capturing:
            image = capture(self.camera)
            self.display_frame(image)

    def on_button_press(self, instance):
        # Stop the camera stream
        self.is_capturing = False
        # Take a picture and save it to a file
        image = capture(self.camera)
        image_path = get_image_file_name(get_config['train_folder'], self.category)
        print(image_path)
        save_image(image, image_path)
        release_camera(self.camera)
        App.get_running_app().exit()
    
    def display_frame(self, frame):
        # Convert the frame to an image and display it
        buf = cv2.flip(frame, 0).tostring()
        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture

class UploadApp(App):
    def build(self):
        return 

def upload():
    UploadApp().run()