import yaml

from utils.config import get_config

def read_yaml(file_name):
    with open(file_name, 'r') as file:
        contents = yaml.safe_load(file)
    
    return contents

def get_local_text(file_name, text):
    return read_yaml(f"lang/{get_config('language')}/{file_name}")[text]

def get_local_upgrade(upgrade_id=None):
    if upgrade_id:
        return read_yaml(f"lang/{get_config('language')}/upgrades.yaml")[upgrade_id]
    else:
        return read_yaml(f"lang/{get_config('language')}/upgrades.yaml")
