from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

class WindowGrid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="Camera Test"))
        self.image = Image(source="test_image.png")
        self.add_widget(self.image)
        self.take_picture = Button(text="Take picture")
        self.add_widget(self.take_picture)
        

class KivyTestApp(App):
    def build(self):
        return WindowGrid()
    
if __name__ == "__main__":
    KivyTestApp().run()