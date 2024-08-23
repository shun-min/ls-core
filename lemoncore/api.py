import requests

from typing import Any, Dict, Optional


class URL:
    project = r"skyline/projects?assigned_to=1940"
    all_shots = r"skyline/shots"
    all_assets = r"skyline/assets"
    assets_by_episode = r"skyline/shots?episode="
    shots_by_episode = r"skyline/shots?episode="


class API():
    version = "api/v1"
    host = "http://127.0.0.1:8000"
    header = {
        "Authorization": "Token 90b073429732f60bcabbf9a6aeed8f5ffb8ebd3e",
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
            headers=cls.header,
        )
        return response
    