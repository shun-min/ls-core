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
        return

    def get_assets(self) -> None:
        response = API._get(url=URL.all_assets)
        return response

    def get_all_shots(self) -> None:
        print("getting shots")

    def get_shots_by_episode(
        self,
        episode: int,
        expand: Optional[List[str]] = [],
    ) -> None:
        response = API._get(url=URL.shots_by_episode(episode=episode))
        return response


class Publisher(object):
    def __init__(self):
        super().__init__()
        self.versions = List[VersionModel]

    def add_files(self):
        print("add_files")

    def add_keys(self, value: List[str]):
        print("add keys")

    def publish(self):
        return
