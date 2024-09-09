import requests

from typing import Any, Dict, Optional

from .models import (
    ContentType,
)

class URL:
    assigned_projects = r"skyline/projects?assigned_to=1940"
    all_shots = r"skyline_content/shots/"
    all_assets = r"skyline_content/assets/"

    @classmethod
    def project(
        cls,
        name: str,
    ):
        return rf"skyline/project?name={name}"

    def get_episode_id():
        return

    @classmethod
    def shots_by_episode(
        cls,
        episode: int
    ) -> str:

        return rf"skyline_content/shots?episode_id={episode}"

    @classmethod
    def file(
        cls,
        version_id: int
    ) -> str:

        return rf"skyline/files?version_id={version_id}"

    @classmethod
    def get_content(
        cls,
        project_name: str,
        type: ContentType,
        name: str,
    ) -> Dict[str: Any]:
        project_id = Project.get(name=project_name)
        return rf"skyline/{type}?project_id={project_id}&"

class API():
    version = "api/v1"
    host = "http://127.0.0.1:8000"
    _header: Dict[str, str] = {
        "Authorization": "Token 90b073429732f60bcabbf9a6aeed8f5ffb8ebd3e"
    }

    @classmethod
    def _get(
        cls,
        url: str,
    ):
        full_url = f"{cls.host}/{cls.version}/{url}"
        print(f"URL: {full_url}")
        response = requests.get(
            url=full_url,
            headers=cls._header,
        )
        return response
