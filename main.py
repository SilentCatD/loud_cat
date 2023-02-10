import asyncio
import json
import logging

import discord
from discord.ext.commands import Bot, when_mentioned_or

import os
from dotenv import load_dotenv

# CRITICAL = 50
# ERROR = 40
# WARNING = 30
# INFO = 20
# DEBUG = 10
# NOTSET = 0

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
f = open("settings.json")

settings = json.load(f)
prefix = settings["prefix"]
reply_when_mentioned = settings["reply_when_mentioned"]
log_level = settings["log_level"]
f.close()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

discord.utils.setup_logging(level=log_level)
bot = Bot(command_prefix=when_mentioned_or(prefix) if reply_when_mentioned else prefix, intents=intents)


@bot.event
async def on_ready():
    logging.log(
        msg=f"{bot.user} is ready! "
            f"Settings: {settings}",
        level=logging.INFO)


async def load_cogs():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f"cogs.{file[:-3]}")


async def main():
    await load_cogs()
    await bot.start(BOT_TOKEN)


asyncio.run(main())
