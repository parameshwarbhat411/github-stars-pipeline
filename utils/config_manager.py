import os
import json
import logging


class ConfigLoader:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', self.config_file)
        logging.info(f"Loading configuration from: {config_path}")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config

    def get(self, key, default=None):
        return self.config.get(key, default)


class DataPathManager:
    def __init__(self, config_loader):
        self.config_loader = config_loader

    def get_data_path(self, key):
        data_path = self.config_loader.get(key)
        if not data_path:
            raise ValueError('Data directory is not set in the configuration')
        return data_path
