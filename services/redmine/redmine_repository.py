from services.redmine.repositories.redmine_project_repository import RedmineProjectRepository


class RedmineRepository:
    def __init__(self, api_key: str, url: str):
        self.api_key = api_key
        self.url = url
        self.project_repository = RedmineProjectRepository(api_key=api_key, url=url)
