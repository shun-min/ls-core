import json
from pathlib import Path


class Utils():
    @classmethod
    def json_load(cls, path: Path):
        try:
            with open(path, "r") as x:
                json_obj = json.load(x)
        except Exception as e:
            print(e)
        return json_obj