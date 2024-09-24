import json
from pathlib import Path

from lemonsky.common.constants import (
    RESOURCES_ROOT,
)

class Utils():
    @classmethod
    def load_settings(cls):
        try:
            with open(RESOURCES_ROOT / "settings.json", "r") as x:
                json_obj = json.load(x)
                return json_obj
        except Exception as e:
            print(e)
            return None
