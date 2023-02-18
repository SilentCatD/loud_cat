from typing import Mapping
import utils


class RedmineComponentRepository:
    def __init__(self, api_key: str, url: str):
        self.api_key = api_key
        self.url = url

    def build_url(self, path: str, params: Mapping) -> str:
        if params is None:
            params = {}
        params["key"] = self.api_key
        return utils.build_url(url=self.url, path=path, params=params)
