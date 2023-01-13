from betterconf.config import AbstractProvider
import json


class JSONProvider(AbstractProvider):
    SETTINGS_JSON_FILE = "settings.json"

    def __init__(self):
        with open(self.SETTINGS_JSON_FILE, "r") as f:
            self._settings = json.load(f)

    def get(self, name):
        return self._settings.get(
            name)
