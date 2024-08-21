import requests

        
class API():
    def __init__(
        self,
    ):
        super().__init__()
        self.set_host()
        self.set_api_version()

    def set_api_version(self):
        self.api_version = "api/v1/"
    
    def set_host(self):
        self.host = "http://127.0.0.1:8000/"


class ProjectAPI(API):
    url = "/projects/"