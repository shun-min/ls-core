from typing import Dict, List

from ..data.dashboard.models import (
    ProjectModel,
    TaskModel,
)

class ToolContext():
    def __init__(self):
        super().__init__()
        self.assigned_projects: List[ProjectModel] = []
        self.active_project: ProjectModel = None
        self.active_task: TaskModel = None