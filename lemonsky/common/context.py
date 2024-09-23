import os, sys
from typing import Any, Dict, List, Optional

import django

from ..data.dashboard.models import (
    ProjectModel,
    TaskModel,
    VersionModel,
)


class ToolContext():
    def __init__(self):
        super().__init__()
        self.init_context()

    def init_context(self) -> None:
        """
        Init django LemonCORE-Web context,
        fetch current task, current user, PC name etc

        """
        sys.path.append(r"N:\pipeline\Tech_team\repo\LemonCORE-Web")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lemoncore.settings')
        django.setup()
        print("Initialized django ORM")

    def fetch_task_context():
        return

    def fetch_current_user():
        return

    def fetch_machine_name():
        return


class Publisher(object):
    """
    Publisher object that controls the registering of versions and files
    Args:
        object (_type_): _description_
    """
    def __init__(self):
        super().__init__()
        self.versions = List[VersionModel]

    def add_files(self):
        print("add_files")

    def publish(self):
        return
