from pathlib import Path
import yaml

from utils.config import get_config

MODULE_ROOT = Path(__file__).parent.parent

def read_yaml(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    
    return data

def write_yaml(data, file_name):
    with open(file_name, 'w') as file:
        yaml.safe_dump(data, file)

def get_local_text(file_name, text):
    return read_yaml(MODULE_ROOT / 'lang' / get_config('language') / file_name)[text]

def get_local_upgrade(upgrade_id=None):
    if upgrade_id:
        return read_yaml(MODULE_ROOT / 'lang' / get_config('language') / 'upgrades.yaml')[upgrade_id]
    else:
        return read_yaml(MODULE_ROOT / 'lang' / get_config('language') / 'upgrades.yaml')
