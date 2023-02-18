import logging

import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.errors import ExtensionError


class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.log(msg=f"{self.__class__.__name__} loaded!", level=logging.INFO)

    @commands.command()
    async def reload_cogs(self, ctx: Context):
        cogs = list(self.bot.extensions.keys())
        async with ctx.typing():
            loaded: list[str] = []
            for cog in cogs:
                try:
                    await self.bot.reload_extension(cog)
                except ExtensionError:
                    await ctx.send(f"Error reloading {cog}")
                    return
                loaded.append(cog)
        embed = discord.Embed(title=f'Cogs reloaded: \n{"#".join(loaded)}'.replace("#", "\n").replace("cogs.", "- "))
        await ctx.send(embed=embed)

    @commands.command()
    async def reload_cog(self, ctx: Context, cog_name: str):
        cogs = self.bot.extensions.keys()
        resolved_cog_name = f"cogs.{cog_name}"
        if resolved_cog_name not in cogs:
            await ctx.send(f"Cog `{cog_name}` not existed")
            return
        async with ctx.typing():
            try:
                await self.bot.reload_extension(resolved_cog_name)
            except ExtensionError:
                await ctx.send(f"Error reloading {cog_name}")
                return
        embed = discord.Embed(title=f'Cogs reloaded: \n-{cog_name}')
        await ctx.send(embed=embed)

    @commands.command()
    async def cogs(self, ctx: Context):
        cogs = list(self.bot.extensions.keys())
        embed = discord.Embed(
            title=f'Cogs reloaded: \n{"#".join(cogs)}'.replace("#", "\n").replace("cogs.", "- "))
        await ctx.send(embed=embed)

    @commands.command()
    async def load_cog(self, ctx: Context, cog_name: str):
        resolved_cog_name = f"cogs.{cog_name}"
        async with ctx.typing():
            try:
                await self.bot.load_extension(resolved_cog_name)
            except ExtensionError:
                await ctx.send(f"Error loading cog `{cog_name}`")
                return
        embed = discord.Embed(title=f'Cog loaded: \n-{cog_name}')
        await ctx.send(embed=embed)

    @commands.command()
    async def sync(self, ctx: Context):
        sync = await ctx.bot.tree.sync()
        await ctx.send(f"Synced {len(sync)} commands.")

    async def cog_check(self, ctx: Context) -> bool:
        pass


async def setup(bot: commands.Bot):
    cog = AdminCog(bot)
    logging.info(f"{cog.__class__.__name__} loading...")
    await bot.add_cog(cog)
