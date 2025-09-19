import discord
from discord.ext import commands
import os
from config import BOT
from components.start import StartExchange
from utils.status import status, activity

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
commands_folder = BOT["COGS_FOLDER"]


@bot.event
async def on_ready():
    print(f'Started - {bot.user} (ID: {bot.user.id})')
    
    bot_status = status(BOT)
    activity = activity(BOT)
    
    await bot.change_presence(
        status=bot_status,
        activity=activity
    )

def load_extensions():
    for filename in os.listdir(commands_folder):
        if filename.endswith(".py"):
            bot.load_extension(f"commands.{filename[:-3]}")
            print(f"Loaded - {filename[:-3]}")
    bot.load_extension("utils.restore") # remove this if your bot doesn't have any components


if __name__ == "__main__":
    load_extensions()
    bot.run(BOT["TOKEN"])
