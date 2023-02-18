from typing import Optional

from utils import parse_date


class Project:
    def __init__(self, project_id: Optional[int], name: Optional[str], description: Optional[str],
                 identifier: Optional[str],
                 created_on: Optional[str], updated_on: Optional[str], url: Optional[str]):
        self.project_id = project_id
        self.name = name
        self.description = description
        self.identifier = identifier
        self.created_on = parse_date(created_on)
        self.updated_on = parse_date(updated_on)
        self.url = url


class ProjectList:
    def __init__(self, projects: list[Project], total_count: int, offset: int, limit: int):
        self.projects = projects
        self.total_count = total_count
        self.offset = offset
        self.limit = limit
