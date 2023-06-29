from kivy.app import App

from modules.train_your_model_game import TrainYourModelGame

class TrainYourModelApp(App):
    def build(self):
        return TrainYourModelGame()
    
    def on_stop(self):
        self.root.save_state()

        return super().on_stop()

if __name__ == "__main__":
    TrainYourModelApp().run()
