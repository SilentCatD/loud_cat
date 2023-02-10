import logging

import discord
from discord.ext import commands
from discord.ext.commands import Context


class GeneralCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.log(msg=f"{self.__class__.__name__} loaded!", level=logging.INFO)

    @commands.command()
    async def ping(self, ctx: Context):
        await ctx.send(f"Pong! In {round(self.bot.latency * 1000, 2)}ms")


async def setup(bot: commands.Bot):
    cog = GeneralCog(bot)
    logging.info(f"{cog.__class__.__name__} loading...")
    await bot.add_cog(cog)
