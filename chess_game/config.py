import json
import os


class Config:
    def __init__(self):
        self.settings = self.load_settings()

    def load_settings(self):
        config_path = os.path.join("configs", "settings.json")
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.settings
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value


config = Config()