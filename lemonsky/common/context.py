from typing import Any, Dict, List, Optional

from ..data.dashboard.models import (
    ProjectModel,
    TaskModel,
    VersionModel,
)

from ..data.dashboard.url_wrapper import (
    API,
    URL,
)
from ..data.dashboard.controllers import (
    Project,
)

class ToolContext():
    def __init__(self):
        super().__init__()
        self.assigned_projects: List[ProjectModel] = []
        self.active_project: ProjectModel = None
        self.active_task: TaskModel = None

    def init_context():
        """
        Init django LemonCORE-Web context,
        fetch current task, current user, PC name etc
        
        """
        return

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
