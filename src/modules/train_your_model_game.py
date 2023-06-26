from kivy.lang.builder import Builder
from kivy.config import Config
from kivy.properties import DictProperty
from kivy.uix.widget import Widget

from modules.training import *
from modules.evaluation import *
from modules.upgrades import *

Builder.load_file("graphics/frame.kv")
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class TrainYourModelGame(Widget):
    state = DictProperty({
        'coins': 0,
        'active_upgrades': set(), # grayscale, resize, contrast, image_generation, train_test_split
        'show_transformations_switch': None,
        'evaluations': []
    })

    def add_coins(self, coins):
        self.state['coins'] += coins
        self.ids.coins_label.text = f"Coins: {self.state['coins']}"