import asyncio
import datetime
import discord
import configparser
import os
import time
import traceback
import logging

from discord.ext import commands
from discord.ext.commands import BucketType, BadArgument
from discord import abc
from discord.abc import PrivateChannel
from utils import Util, Configuration
from argparse import ArgumentParser

bot = commands.Bot(command_prefix=">", description='The bot to help with various duties such as LFG, Pullroom, and Etc!')

bot.starttime = datetime.datetime.now()
bot.startup_done = False

initial_extensions = ['lookingfor', 'moderation', 'admin']

if not os.path.exists('config'):
    os.makedirs('config')

TOKEN = "token"

@bot.event
async def on_command_error(ctx: commands.Context, error):
    logs = bot.get_channel(712640778136059975)
    if isinstance(error, commands.CommandOnCooldown):        
        cool = await ctx.send("It looks like that someone has used the emergency ping recently. Please wait for a bit before trying again, if it's urgent then please contact the mods at <@711678018573303809>")
        await asyncio.sleep(15)
        await cool.delete()
        await ctx.message.delete()
        raise error
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send("This bot command is not meant for private messages!")
    elif isinstance(error, commands.BotMissingPermissions):
        embed=discord.Embed(title="Bot missing permission", description=f"{ctx.author} (``{ctx.author.id}``) just tried to use the command, but I was not able to complete it without the required permission.\n**Message Context**:\n{ctx.message.context}", color=0xfffca8)
        embed.set_footer(text=f"{ctx.author} in {ctx.server.name}")
        await logs.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        return
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        await logs.send(f"Command execution failed:\n"
                                    f"    Command: {ctx.command}\n"
                                    f"    Message: {ctx.message.content}\n"
                                    f"    Channel: {'Private Message' if isinstance(ctx.channel, abc.PrivateChannel) else ctx.channel.name}\n"
                                    f"    Sender: {ctx.author.name}#{ctx.author.discriminator}\n"
                                    f"    Exception: {error}")
        await ctx.send(":rotating_light: Something went wrong while executing that command. Please double check your command to see what happened, if it still persists - please contact Ghoul asap. :rotating_light:")

        embed = discord.Embed(colour=discord.Colour(0xff0000),
                            timestamp=datetime.datetime.utcfromtimestamp(time.time()))

        embed.set_author(name="Command execution failed:")
        embed.add_field(name="Command", value=ctx.command)
        embed.add_field(name="Original message", value=Util.trim_message(ctx.message.content, 1024))
        embed.add_field(name="Channel",
                        value='Private Message' if isinstance(ctx.channel, abc.PrivateChannel) else f"{ctx.channel.name} ({ctx.channel.id})")
        embed.add_field(name="Sender", value=f"{ctx.author.name}#{ctx.author.discriminator}")
        embed.add_field(name="Exception", value=error)
        v = ""
        for line in traceback.format_tb(error.__traceback__):
            if len(v) + len(line) > 1024:
                embed.add_field(name="Stacktrace", value=v)
                v = ""
            v = f"{v}\n{line}"
        if len(v) > 0:
            embed.add_field(name="Stacktrace", value=v)
            await logs.send(embed=embed)

async def on_error(event, *args, **kwargs):
    # something went wrong and it might have been in on_command_error, make sure we log to the log file first
    logs = bot.get_channel(712640778136059975)
    await logs.send(f"error in {event}\n{args}\n{kwargs}")
    embed = discord.Embed(colour=discord.Colour(0xff0000),
                          timestamp=datetime.datetime.utcfromtimestamp(time.time()))

    embed.set_author(name=f"Caught an error in {event}:")

    embed.add_field(name="args", value=str(args))
    embed.add_field(name="kwargs", value=str(kwargs))
    embed.add_field(name="cause message", value=traceback._cause_message)
    v = ""
    for line in traceback.format_exc():
        if len(v) + len(line) > 1024:
            embed.add_field(name="Stacktrace", value=v)
            v = ""
        v = f"{v}{line}"
    if len(v) > 0:
        embed.add_field(name="Stacktrace", value=v)

    await logs.send(embed=embed)
    # try logging to botlog, wrapped in an try catch as there is no higher lvl catching to prevent taking donwn the bot (and if we ended here it might have even been due to trying to log to botlog
    try:
        pass
    except Exception as ex:
        await logs.send(
            f"Failed to log to botlog, either discord broke or something is seriously wrong!\n{ex}")
        await logs.send(traceback.format_exc())

async def on_connect(self):
    logs = bot.get_channel(712640778136059975)
    embed = discord.Embed(colour=discord.Colour(0x77dd77),title='Connected to gateway', description=f"{self.bot.user.name} has connected to the gateway!",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
    await logs.send(embed=embed)

async def on_disconnect(self):
    logs = bot.get_channel(712640778136059975)
    embed = discord.Embed(colour=discord.Colour(0xff0000),title='Disconnected from gateway', description=f"{self.bot.user.name} has disconnected from the gateway, blame Discord!",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
    await logs.send(embed=embed)
        
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(f"cogs.{extension}")

#if __name__ == '__main__':
    #parser = ArgumentParser()
    #parser.add_argument("--token", help="Specify your Discord token")

    #clargs = parser.parse_args()
    #if 'botlogin' in os.environ:
    #    token = os.environ['botlogin']
    #elif clargs.token:
    #    token = clargs.token
    ##else:
    #   token = input("Please enter your Discord token: ")

@bot.event
async def on_ready():
    if not bot.startup_done:
        await Configuration.onReady(bot)
        logs = bot.get_channel(712640778136059975)
        embed = discord.Embed(colour=discord.Colour(0x77dd77),title='Successfully connected to the gateway', description=f"{bot.user.name} has connected to the gateway!",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
        await logs.send(embed=embed)
        print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}' + f'\nVersion: {discord.__version__}\n')
        await bot.change_presence(activity=discord.Activity(name='VALORANT', type=discord.ActivityType.watching))

bot.run(TOKEN)

