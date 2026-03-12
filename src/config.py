import os
import json
import socket

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'settings.json')

class ConfigManager:
    _loaded = False
    _config = {}

    @classmethod
    def load(cls):
        if not cls._loaded:
            cls._config = {
                'display_name': socket.gethostname(),
                'theme': 'system'
            }
            if os.path.exists(CONFIG_FILE):
                try:
                    with open(CONFIG_FILE, 'r') as f:
                        data = json.load(f)
                        cls._config.update(data)
                except Exception:
                    pass
            cls._loaded = True

    @classmethod
    def get(cls, key, default=None):
        cls.load()
        return cls._config.get(key, default)

    @classmethod
    def set(cls, key, value):
        cls.load()
        cls._config[key] = value
        cls.save()

    @classmethod
    def save(cls):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(cls._config, f, indent=4)
        except Exception:
            pass
