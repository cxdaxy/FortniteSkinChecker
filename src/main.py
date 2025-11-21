import os
import pathlib

import discord
import sentry_sdk
from discord.ext import commands

from config import Settings


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=Settings.BOT_PREFIX, intents=discord.Intents.default()
        )

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user}")
        print(f"Connected to {len(self.guilds)}")

    async def setup_hook(self) -> None:
        if Settings.PRODUCTION:
            sentry_sdk.init(
                dsn=Settings.DSN,
                traces_sample_rate=1.0,
                profiles_sample_rate=1.0,
            )

        await self.load_cogs()
        await self.tree.sync()

    async def load_cogs(self, dir: str = "src/commands") -> None:
        path = pathlib.Path().resolve() / dir
        for file in os.listdir(path):
            if file.endswith(".py"):
                cog = file[:-3]
                await self.load_extension(f"commands.{cog}")
                print(f"Cog {cog} loaded successfully")


def start_bot() -> None:
    try:
        bot = Bot()
        bot.run(token=Settings.DISCORD_TOKEN)
    except Exception as e:
        print(f"An error occurred while starting the bot: {e}")


if __name__ == "__main__":
    start_bot()
