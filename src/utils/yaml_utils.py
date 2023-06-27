import yaml

def read_yaml(file_name):
    with open(file_name, 'r') as file:
        contents = yaml.safe_load(file)
    
    return contents
