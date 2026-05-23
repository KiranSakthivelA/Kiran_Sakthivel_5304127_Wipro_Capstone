import configparser
import os

def get_config(section, key):
    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.properties")
    config.read(config_file_path)
    return config.get(section, key)
