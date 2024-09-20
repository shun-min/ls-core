import json
import requests

from typing import Any, Dict, List, Optional

from lemonsky.common.constants import (
    METADATA_PATH,
    RESOURCES_ROOT,
)
from lemonsky.common.helpers import (
    Utils
)
from lemonsky.common.singleton import Singleton

from lemonsky.common.enums import (
    HOST,
)
from .models import (
    ContentTypeEnums,
    TaskModel,
)

class URL:
    assigned_projects = r"skyline/projects?assigned_to=1940"
    all_shots = r"skyline_content/shots/"
    all_assets = r"skyline_content/assets/"

    @classmethod
    def get_project(
        cls,
        code: str,
    ) -> str:
        return rf"skyline/projects?code={code}"

    @classmethod
    def get_step(
        cls,
        code: str,
    ) -> str:
        return rf"skyline/steps?code={code}"      
    
    @classmethod
    def get_shots_by_episode(
        cls,
        episode: int
    ) -> str:
        return rf"skyline_content/shots?episode_id={episode}"

    @classmethod
    def get_content(
        cls,
        project_id: int,
        type: ContentTypeEnums,
        name: str,
    ) -> str:
        return rf"skyline/{type}?project_id={project_id}&"

    @classmethod
    def get_shot(
        cls,
        shot_code: str,
        project_id: int,
    ) -> str:
        return rf"skyline_content/shots?shot_code={shot_code}&project_id={project_id}"

    @classmethod
    def get_task(
        cls,
        content_type: str,
        content_id: int,
        step_id: int,
    ) -> str:
        return rf"skyline/tasks?project_content_type={content_type}&content_id={content_id}&step_id={step_id}"
    
    @classmethod
    def get_version(
        cls,
        task_id: str,
    ) -> str:
        return rf"skyline/versions?task_id={task_id}"

    @classmethod
    def file(
        cls,
        keys: Optional[List[str]] = [],
        parent: Optional[int] = None,
        setting_keyword: Optional[str] = "",
        version_type: Optional[str] = "skylineversion",
        version_id: Optional[int] = None,
    ) -> str:
        full_url = rf"skyline/files?"
        if version_id:
            full_url = full_url + f"version_type={version_type}&version_id={version_id}&"

        if keys:
            key_params = ",".join(keys)
            full_url = full_url + f"keys={key_params}&"

        if setting_keyword:
            full_url = full_url + f"setting_keyword={setting_keyword}&"

        if parent:
            full_url = full_url + f"parent={parent}"

        if full_url.endswith("&"):
            full_url = full_url.strip("&")
        
        return full_url

class APIConfig(Singleton):
    def __init__(self) -> None:
        super().__init__()
        self.metadata = self.get_metadata()
        self._host = self._set_host()
        self._version = self._set_version()
        self._header = self._set_header()

    def get_metadata(self):
        json_obj = Utils.json_load(path=METADATA_PATH)
        return json_obj

    def _set_host(self):
        host = "https://lemoncore.lemonskystudios.com"
        if self.metadata["HOST"] == HOST.DEV:
            host = "http://127.0.0.1:8000"
        return host

    def _set_version(self):
        return "api/v1"
    
    def _set_header(self)-> Dict[str, str]:
        settings_path = RESOURCES_ROOT / "settings.json"
        json_obj = Utils.json_load(path=settings_path)
        return json_obj["HEADER"]

    def _get(
        self,
        url: str,
    ):
        full_url = f"{self._host}/{self._version}/{url}"
        print(f"URL: {full_url}")
        response = requests.get(
            url=full_url,
            headers=self._header,
        )
        if not response.ok:
            response.raise_for_status()
        result = response.json()
        return result
