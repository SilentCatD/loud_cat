from typing import Any
from services.redmine.models.project import *
from urllib.parse import urlparse, urljoin


class ProjectConverter:
    def __init__(self, data: Any, url: str):
        self.data = data
        self.url = url

    def convert(self) -> Project:
        data = self.data
        return Project(project_id=data["id"],
                       name=data["name"],
                       identifier=data['identifier'],
                       description=data['description'],
                       created_on=data['created_on'],
                       updated_on=data['updated_on'],
                       url=urljoin(urlparse(self.url + 'projects/').geturl(),
                                   url=data['identifier']))


class ProjectListConverter:
    def __init__(self, data: Any, url: str):
        self.data = data
        self.url = url

    def convert(self) -> ProjectList:
        data = self.data
        project_results: list[Project] = []
        projects = data["projects"]
        for project in projects:
            parsed = ProjectConverter(project, self.url).convert()
            project_results.append(parsed)
        return ProjectList(projects=project_results, total_count=data["total_count"], offset=data["offset"],
                           limit=data["limit"])
