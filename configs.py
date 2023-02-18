import json
import os
from dotenv import load_dotenv


# CRITICAL = 50
# ERROR = 40
# WARNING = 30
# INFO = 20
# DEBUG = 10
# NOTSET = 0

class BotConfig:
    def __init__(self):
        load_dotenv()
        bot_token = os.getenv("BOT_TOKEN")
        redmine_api_key = os.getenv("REDMINE_API_KEY")

        f = open("settings.json")
        settings = json.load(f)
        prefix = settings["prefix"]
        reply_when_mentioned = settings["reply_when_mentioned"]
        log_level = settings["log_level"]
        redmine_url = settings["redmine_url"]
        f.close()

        self.prefix: str = prefix
        self.reply_when_mentioned: bool = reply_when_mentioned
        self.log_level: int = log_level
        self.redmine_url: str = redmine_url
        self.bot_token: str = bot_token
        self.redmine_api_key: str = redmine_api_key


bot_config = BotConfig()
