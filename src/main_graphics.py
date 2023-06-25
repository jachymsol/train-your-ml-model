from kivy.app import App

from modules.train_your_model_game import TrainYourModelGame

class TrainYourModelApp(App):
    def build(self):
        return TrainYourModelGame()

if __name__ == "__main__":
    TrainYourModelApp().run()
