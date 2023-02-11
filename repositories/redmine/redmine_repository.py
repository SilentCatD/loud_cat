import datetime
import logging
from typing import Optional

import motor.motor_asyncio as motor
from aiohttp import ClientSession
import urllib.parse as urlparse
from urllib.parse import urlencode, urljoin


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


class RedmineRepository:
    def __init__(self, url: str, api_key: str, mongo_username: str, mongo_password: str, mongo_cluster_address: str):
        self.url = url
        self.api_key = api_key
        url = f"mongodb+srv://{mongo_username}:{mongo_password}@{mongo_cluster_address}/?retryWrites=true&w=majority"
        client = motor.AsyncIOMotorClient(url)
        self.db = client.noisy_cat.user_ids

    def build_url(self, path: str, params=None) -> str:
        if params is None:
            params = {}
        params['key'] = self.api_key
        url = self.url + path
        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)

        url_parts[4] = urlencode(query)

        return urlparse.urlunparse(url_parts)

    async def get_all_projects(self, offset: int = None, limit: int = None) -> Optional[ProjectList]:
        async with ClientSession() as session:
            params = {}
            if offset is not None:
                params['offset'] = offset
            if limit is not None:
                params['limit'] = limit
            url = self.build_url('projects.json', params)
            async with session.get(url) as resp:
                if resp.status == 200:
                    results = await resp.json()
                    projects: list[Project] = []
                    for result in results['projects']:
                        parsed = Project(project_id=result["id"], name=result["name"], identifier=result['identifier'],
                                         description=result['description'], created_on=result['created_on'],
                                         updated_on=result['updated_on'],
                                         url=urljoin(urlparse.urlparse(self.url + 'projects/').geturl(),
                                                     url=result['identifier']))
                        projects.append(parsed)
                    return ProjectList(projects=projects, total_count=results["total_count"], offset=results["offset"],
                                       limit=results["limit"])
                return None

    async def save_user_id(self, discord_id: int, user_id: int):
        await self.db.update_one(filter={
            "_id": discord_id
        }, update={
            "$set": {
                "user_id": user_id,
            }
        }, upsert=True)

    async def get_user_id(self, discord_id: int) -> Optional[int]:
        data = {
            "_id": discord_id
        }
        result = self.db.find_one(data)
        result = await result
        logging.info(result)
        if result:
            return result["user_id"]


def parse_date(date: Optional[str]) -> Optional[datetime.datetime]:
    if date is None:
        return None
    try:
        return datetime.datetime.fromisoformat(date[:-1]).astimezone(datetime.timezone.utc)
    except ValueError:
        return None
