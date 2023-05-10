import kivy

from kivy.app import App
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock

import cv2

class CameraClick(BoxLayout):

    def __init__(self, **kwargs):
        super(CameraClick, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Create a widget to display the camera output
        self.img = Image()
        self.add_widget(self.img)

        # Create a button to take a picture
        self.button = Button(text='Take Picture', size_hint=(1, 0.2))
        self.button.bind(on_press=self.on_button_press)
        self.add_widget(self.button)

        # Initialize the camera
        self.capture = cv2.VideoCapture(0)
        self.is_capturing = True
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        if self.is_capturing:
            # Get the latest camera frame
            ret, frame = self.capture.read()

            if ret:
                frame = self.crop_frame_to_square(frame)

                self.display_frame(frame)

    def on_button_press(self, instance):
        # Stop the camera stream
        self.is_capturing = False
        # Take a picture and save it to a file
        ret, frame = self.capture.read()
        if ret:
            frame = self.crop_frame_to_square(frame)

            self.display_frame(frame)

            # Save the captured image to a file
            cv2.imwrite('picture.png', frame)

            # Release the camera and display the captured image
            self.capture.release()
    
    def crop_frame_to_square(self, frame):
        # Crop the frame to a square
        h, w = frame.shape[:2]
        min_dim = min(h, w)
        start_x = (w - min_dim) // 2
        start_y = (h - min_dim) // 2
        return frame[start_y:start_y+min_dim, start_x:start_x+min_dim]

    def display_frame(self, frame):
        # Convert the frame to an image and display it
        buf = cv2.flip(frame, 0).tostring()
        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture


class CameraApp(App):

    def build(self):
        return CameraClick()

if __name__ == '__main__':
    CameraApp().run()
