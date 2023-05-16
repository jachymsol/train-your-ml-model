from kivy.app import App
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
import cv2

from utils.upload_utils import *
from utils.config import get_config

class UploadBox(BoxLayout):
    def __init__(self, **kwargs):
        super(UploadBox, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Create a widget to display the camera output
        self.img = Image()
        self.add_widget(self.img)

        # Create a dropdown to choose the category
        self.category_spinner = Spinner(
            text=get_config("categories")[0],
            values=get_config("categories")
        )
        self.add_widget(self.category_spinner)

        # Create a button to take a picture
        self.button = Button(text='Take Picture', size_hint=(1, 0.2))
        self.button.bind(on_press=self.on_button_press)
        self.add_widget(self.button)

        # Initialize the camera
        self.camera = create_camera()
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
        image_path = get_image_file_name(get_config('train_folder'), self.category_spinner.text)
        print(image_path)
        save_image(image, image_path)
        release_camera(self.camera)
        App.get_running_app().stop()
    
    def display_frame(self, frame):
        # Convert the frame to an image and display it
        buf = cv2.flip(frame, 0).tostring()
        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture

class UploadApp(App):
    def build(self):
        return UploadBox()

def upload():
    UploadApp().run()