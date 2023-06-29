from pathlib import Path
import yaml

CONFIG_LOCATION = Path(__file__).parent.parent / 'config.yaml'

def init_config():
    with open(CONFIG_LOCATION, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    return config

CONFIG = init_config()

def print_config():
    print(CONFIG)

def get_config(key):
    return CONFIG[key]

def set_config(key, value):
    CONFIG[key] = value

def save_config():
    with open(CONFIG_LOCATION, 'w') as config_file:
        yaml.safe_dump(CONFIG, config_file)
