import asyncio
import json
import logging
import os
import typing

import discord
from discord import ui

from repositories.redmine.redmine_repository import *

from discord.ext import commands, menus
from discord.ext.commands import Context


class ProjectsSources(menus.ListPageSource):
    def __init__(self, data: list[Project], total_count: int, offset: int, limit: int):
        self.total_count = total_count
        self.offset = offset
        self.limit = limit
        super().__init__(data, per_page=4)

    async def format_page(self, menu: menus.MenuPages, entries: list[Project]):
        embed = discord.Embed(title=f"Projects : {self.total_count} | Limit {self.limit} | Offset: {self.offset}",
                              description=f"Page {menu.current_page + 1}/{self.get_max_pages()}",
                              timestamp=datetime.datetime.now())
        for entry in entries:
            embed.add_field(name="",
                            value=f"[{entry.project_id} - {entry.name}]({entry.url})\n"
                                  f"created: {entry.created_on.strftime('%d-%m-%Y %H:%M')}\n"
                                  f"updated: {entry.updated_on.strftime('%d-%m-%Y %H:%M')}",
                            inline=False)
        embed.set_footer(text=f"Requested by: {menu.ctx.author}")
        return embed


class RedmineCommandFlags(commands.FlagConverter, prefix="-", delimiter=" "):
    create: typing.Optional[int]


class RedmineCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        f = open("settings.json")
        settings = json.load(f)
        redmine_url = settings["redmine_url"]
        f.close()
        redmine_api_key = os.getenv("REDMINE_API_KEY")
        mongo_username = os.getenv("MONGO_USERNAME")
        mongo_password = os.getenv("MONGO_PASSWORD")
        mongo_cluster = os.getenv("MONGO_CLUSTER_ADDRESS")
        self.repository = RedmineRepository(url=redmine_url, api_key=redmine_api_key, mongo_username=mongo_username,
                                            mongo_password=mongo_password, mongo_cluster_address=mongo_cluster)

    @commands.Cog.listener()
    async def on_ready(self):
        logging.log(msg=f"{self.__class__.__name__} loaded!", level=logging.INFO)

    @commands.command()
    async def redmine(self, ctx: Context, user: typing.Optional[typing.Union[discord.Member, int]], *,
                      flags: RedmineCommandFlags):
        async with ctx.typing():
            if user is not None:
                discord_user = user
            else:
                discord_user = ctx.author
            if flags.create is None:
                user_id = await self.repository.get_user_id(discord_id=discord_user.id)

                if user_id is None:
                    if user is not None:
                        await ctx.send(
                            "This user haven't register a `redmine id` yet, use `redmine -create <id>` to create "
                            "one")
                    else:
                        await ctx.send(
                            "You haven't register a `redmine id` yet, use `redmine -create <id>` to create one")
                else:
                    await ctx.send(f"{discord_user.mention} has {user_id}")
            else:
                await self.repository.save_user_id(user_id=flags.create, discord_id=discord_user.id)
                await ctx.send(f"Successfully register {discord_user.mention} with `redmine id`: {flags.create}")

    @commands.command()
    async def projects(self, ctx: Context, limit: int = 25, offset: Optional[int] = None):
        async with ctx.typing():
            results = await self.repository.get_all_projects(offset=offset, limit=limit)
            pages = menus.MenuPages(
                source=ProjectsSources(results.projects, total_count=results.total_count, offset=results.offset,
                                       limit=results.limit), clear_reactions_after=True)
        await pages.start(ctx)


async def setup(bot: commands.Bot):
    cog = RedmineCog(bot)
    logging.info(f"{cog.__class__.__name__} loading...")
    await bot.add_cog(cog)
