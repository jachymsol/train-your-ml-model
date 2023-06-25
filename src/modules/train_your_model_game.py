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
        'active_upgrades': set(), # grayscale, resize, contrast, image_generation, train_test_split
        'show_transformations_switch': None,
        'evaluations': []
    })