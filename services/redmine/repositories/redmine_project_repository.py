from services.redmine.repositories.redmine_component_repository import RedmineComponentRepository
from aiohttp import ClientSession
from services.redmine.converter.projects_converter import *


class RedmineProjectRepository(RedmineComponentRepository):
    async def get_projects(self, offset: int = 0, limit: int = 25) -> Optional[ProjectList]:
        params = {'offset': offset, 'limit': limit}
        path = "projects.json"
        url = self.build_url(path, params)
        async with ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    results = await resp.json()
                    converter = ProjectListConverter(results, self.url)
                    return converter.convert()
                else:
                    return None
