from kivy.lang.builder import Builder
from kivy.config import Config
from kivy.uix.widget import Widget
import datetime
from pathlib import Path

from modules.training import *
from modules.evaluation import *
from modules.upgrades import *
from utils.config import get_config
import utils.yaml_utils as yaml_utils

Builder.load_file("graphics/frame.kv")
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

INITIAL_STATE = {
    'language': get_config('language'),
    'coins': get_config('start_coins'),
    'active_upgrades': set(), # grayscale, resize, contrast, image_generation, train_test_split
    'show_transformations': True,
    'evaluations': []
}

class TrainYourModelGame(Widget):
    state = INITIAL_STATE

    def __init__(self, **kwargs):
        load_game = get_config('load_game')
        if not load_game:
            load_game = str(datetime.datetime.now())
        self.state_folder = Path.expanduser(Path(get_config('state_folder'))) / load_game
        Path.mkdir(self.state_folder, parents=False, exist_ok=True)

        if Path.exists(self.state_folder / 'state.yaml'):
            self.state = yaml_utils.read_yaml(self.state_folder / 'state.yaml')

        super().__init__(**kwargs)

    def add_coins(self, coins):
        self.state['coins'] += coins
        self.ids.coins_label.text = str(self.state['coins'])

    def save_state(self):
        yaml_utils.write_yaml(self.state, self.state_folder / 'state.yaml')
