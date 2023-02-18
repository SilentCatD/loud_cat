import asyncio
import logging
import os
from typing import Any
from configs import bot_config
import discord
from discord.ext.commands import Bot, when_mentioned_or


class NoisyCat(Bot):

    def __init__(self, **options: Any):

        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True

        prefix = bot_config.prefix
        command_prefix = when_mentioned_or(
            prefix) if bot_config.reply_when_mentioned else prefix
        super().__init__(command_prefix, intents=intents, **options)

    async def on_ready(self):
        logging.log(
            msg=f"{self.user} is ready!",
            level=logging.INFO)

    async def load_cogs(self):
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                await self.load_extension(f"cogs.{file[:-3]}")


async def run_bot():
    bot_token = bot_config.bot_token
    discord.utils.setup_logging(level=bot_config.log_level)
    bot = NoisyCat()
    await bot.load_cogs()
    await bot.start(bot_token)


if __name__ == '__main__':
    asyncio.run(run_bot())
