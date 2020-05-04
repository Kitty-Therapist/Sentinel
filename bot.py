import asyncio
import datetime
import discord 
import configparser
import os
import traceback

from discord.abc import PrivateChannel
from discord.ext import commands
from discord import utils
from utils import Configuration

if not os.path.exists('config'):
    os.makedirs('config')

TOKEN = "Sweet ol' token"

bot = commands.Bot(command_prefix = "!v")

bot.starttime = datetime.datetime.now()
bot.startup_done = False
bot.help_command = None

initial_extensions = ['main']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(f"cogs.{extension}")

@bot.event
async def on_ready():
    if not bot.startup_done:
        await Configuration.onReady(bot)
        print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}' + f'\nVersion: {discord.__version__}\n')
        await bot.change_presence(activity=discord.Activity(name='Looking for category', type=discord.ActivityType.watching))

bot.run(TOKEN)
