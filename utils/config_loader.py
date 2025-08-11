import yaml

def load_config(config_path: str = 'config/config.yaml'):

    with open(config_path) as file:
        config = yaml.safe_load(file)
    
    return config