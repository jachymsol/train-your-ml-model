from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget

Builder.load_file("graphics/frame.kv")

class TrainYourModelGame(Widget):
    pass

class TrainYourModelApp(App):
    def build(self):
        return TrainYourModelGame()

if __name__ == "__main__":
    TrainYourModelApp().run()
