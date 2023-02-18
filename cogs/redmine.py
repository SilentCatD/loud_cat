import logging
from datetime import datetime
import discord
from discord.ext import commands, menus
from discord.ext.commands import Context

from services.redmine.models.project import Project, ProjectList
from services.redmine.redmine_repository import RedmineRepository
from configs import bot_config


class ProjectsSources(menus.ListPageSource):
    def __init__(self, data: ProjectList, per_page: int):
        self.total_count = data.total_count
        self.offset = data.offset
        self.limit = data.limit
        super().__init__(data.projects, per_page=per_page)

    async def format_page(self, menu: menus.MenuPages, entries: list[Project]):
        embed = discord.Embed(title=f"Projects :",
                              description=f"Page {menu.current_page + 1}/{self.get_max_pages()}",
                              timestamp=datetime.now())
        for entry in entries:
            embed.add_field(name="",
                            value=f"[{entry.project_id} - {entry.name}]({entry.url})\n"
                                  f"{entry.description}",
                            inline=False)
        embed.set_footer(
            text=f"{self.offset * self.limit} - {self.limit * (1 + self.offset)} of total: {self.total_count}")
        return embed


class RedmineProjectsFlags(commands.FlagConverter, prefix="-", delimiter=" "):
    offset: int = commands.flag(name="offset", aliases=["o"], default=0)
    limit: int = commands.flag(name="limit", aliases=["l"], default=25)
    per_page: int = commands.flag(name="per_page", aliases=["pp"], default=4)


class RedmineCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.repository = RedmineRepository(url=bot_config.redmine_url, api_key=bot_config.redmine_api_key)

    @commands.Cog.listener()
    async def on_ready(self):
        logging.log(msg=f"{self.__class__.__name__} loaded!", level=logging.INFO)

    @commands.command()
    async def projects(self, ctx: Context, *, flags: RedmineProjectsFlags):
        async with ctx.typing():
            projects = await self.repository.project_repository.get_projects(offset=flags.offset, limit=flags.limit)
            if projects is None:
                await ctx.send("Something went wrong, unable to fetch projects")
                return

            pages = menus.MenuPages(source=ProjectsSources(projects, per_page=flags.per_page),
                                    clear_reactions_after=True)
            await pages.start(ctx)


async def setup(bot: commands.Bot):
    cog = RedmineCog(bot)
    logging.info(f"{cog.__class__.__name__} loading...")
    await bot.add_cog(cog)
