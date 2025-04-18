import json
import os, sys

from pathlib import Path

import django

from studio.common.constants import (
    RESOURCES_ROOT,
)
from studio.common.singleton import Singleton


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


class Django(Singleton):
    """
    Init django LemonCORE-Web context,
    fetch current task, current user, PC name etc

    """
    settings_json = Utils.load_settings()
    sys.path.append(settings_json["ORM_LOCATION"])
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lemoncore.settings')
    django.setup()
    print("Initialized ORM")