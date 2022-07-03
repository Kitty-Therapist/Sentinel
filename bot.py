import datetime
import os
import time

import discord
from discord.ext import commands
from utils import Configuration

intents = discord.Intents.all()

initial_extensions = ["cogs.pullroom"]

if not os.path.exists('config'):
    os.makedirs('config')

TOKEN = "lol"

class SentinelBot(commands.Bot):
    def __init__(self, command_prefix, **o):
      super().__init__(command_prefix, **o)

    async def setup_hook(self):
        for extensions in initial_extensions:
            await self.load_extension(f'{extensions}')
            print("Loaded!!")

# Create bot instance
client = SentinelBot(">", intents=intents)

@client.event
async def on_ready():
    client.starttime = datetime.datetime.now()
    logs = client.get_channel(712640778136059975)
    embed = discord.Embed(colour=discord.Colour(0x77dd77),title='Successfully connected to the gateway', description=f"{client.user.name} has connected to the gateway!",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
    await logs.send(embed=embed)
    print(f'\n\nLogged in as: {client.user.name} - {client.user.id}' + f'\nVersion: {discord.__version__}\n')
    await client.change_presence(activity=discord.Activity(name='VALORANT', type=discord.ActivityType.watching))

# Start the bot
if __name__ == "__main__":
    client.run(TOKEN)
