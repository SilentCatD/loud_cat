import asyncio
import logging

import discord
from discord import ui
from discord.ext import commands
from discord import app_commands


class LogWorkModal(ui.Modal, title="Log work modal"):
    hours = ui.TextInput(label="Spent time", placeholder="8.8", required=True, max_length=3)
    comment = ui.TextInput(label="Comment", required=True, style=discord.TextStyle.paragraph)


class IssueSelect(ui.View):
    @ui.select(
        min_values=1,
        max_values=1,
        placeholder="Issue",
        options=[
            discord.SelectOption(
                label="Issue 1"
            ),
            discord.SelectOption(
                label="Issue 2"
            ),
            discord.SelectOption(
                label="Issue 3"
            )
        ]
    )
    async def callback(self, interaction: discord.Interaction, select: ui.Select):
        await asyncio.sleep(3)
        await interaction.response.send_modal(LogWorkModal())


class ProjectSelect(ui.View):
    @ui.select(
        min_values=1,
        max_values=1,
        placeholder="Project",
        options=[
            discord.SelectOption(
                label="Project 1"
            ),
            discord.SelectOption(
                label="Project 2"
            ),
            discord.SelectOption(
                label="Project 3"
            )
        ]
    )
    async def callback(self, interaction: discord.Interaction, select: ui.Select):
        await asyncio.sleep(3)
        select.disabled = True
        await interaction.response.send_message(view=IssueSelect())


class RedmineCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.log(msg=f"{self.__class__.__name__} loaded!", level=logging.INFO)

    @app_commands.command(name="log-work")
    async def log_work(self, interaction: discord.Interaction) -> None:
        await interaction.message.edit_message(view=self)
        await interaction.message.send_message(view=IssueSelect())


async def setup(bot: commands.Bot):
    cog = RedmineCog(bot)
    logging.info(f"{cog.__class__.__name__} loading...")
    await bot.add_cog(cog)
