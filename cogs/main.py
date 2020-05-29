import discord
import asyncio
import os
import subprocess
from subprocess import Popen
from discord.ext import commands
from discord import utils

from utils import Configuration 

git = "git pull"

class main(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def restart(self, ctx:commands.Context):
        if ctx.author.id == 298618155281154058:
            await ctx.send("Restarting...")
            await ctx.bot.close()
        else:
            return

    @commands.command(hidden=True)
    async def pull(self, ctx):
        """Pulls from github so an upgrade can be performed without full restart"""
        if ctx.author.id == 298618155281154058:
            async with ctx.typing():
                p = Popen(["git pull"], cwd=os.getcwd(), shell=True, stdout=subprocess.PIPE)
                while p.poll() is None:
                    await asyncio.sleep(1)
                out, error = p.communicate()
                await ctx.send(f"Pull completed with exit code {p.returncode}```yaml\n{out.decode('utf-8')}```")
        else:
            return

    @commands.command(hidden=True)
    async def reload(self, ctx, *, cog: str):
        if ctx.author.id == 298618155281154058:
            cogs = []
            for c in ctx.bot.cogs:
                cogs.append(c.replace('Cog', ''))

            if cog in cogs:
                self.bot.unload_extension(f"cogs.{cog}")
                self.bot.load_extension(f"cogs.{cog}")
                await ctx.send(f'**{cog}** has been reloaded')
            else:
                await ctx.send(f"I can't find that cog.")
        else:
            return

    @commands.command(hidden=True)
    async def load(self, ctx, cog: str):
        if ctx.author.id == 298618155281154058:
            if os.path.isfile(f"cogs/{cog}.py") or os.path.isfile(f"Valorant-LF/cogs/{cog}.py"):
                self.bot.load_extension(f"cogs.{cog}")
                await ctx.send(f"**{cog}** has been loaded!")
            else:
                await ctx.send(f"I can't find that cog.")
        else:
            return

    @commands.command(hidden=True)
    async def unload(self, ctx, cog: str):
        if ctx.author.id == 298618155281154058:
            cogs = []
            for c in ctx.bot.cogs:
                cogs.append(c.replace('Cog', ''))
            if cog in cogs:
                self.bot.unload_extension(f"cogs.{cog}")
                await ctx.send(f'**{cog}** has been unloaded')
            else:
                await ctx.send(f"I can't find that cog.")
        else:
            return
    
    @commands.command()
    async def release(self, ctx:commands.Context):
        """Spam the same message over and over for an hour."""
        log = ctx.guild.get_channel(679877028991860876)
        Mods = discord.utils.get(ctx.guild.roles, id=703063141990400001)
        if 703063141990400001 not in [role.id for role in ctx.author.roles]:
            return
        else:
            await ctx.send("Now sending the release tag in every one and half minutes for an hour!")
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await log.send(":warning::warning: **VALORANT will be released on the 2nd of June, until then you will be unable to access the game. For more information, please go to <#713451899092992031> or <#679877572431314981> for more information.\nAll modes of games have been disabled, and no one is currently able to play Valorant..** :warning::warning:")
            await asyncio.sleep(150)
            await ctx.send("The hour of 1 minute and 30 seconds in each message has been done. Please run ``!vrelease`` if people are still asking.")
            


    @commands.group()
    async def filter(self, ctx:commands.Context):
        """Base commands for the filtered related word list."""
        Mods = discord.utils.get(ctx.guild.roles, id=703063141990400001)
        if 703063141990400001 not in [role.id for role in ctx.author.roles]:
            return
        else:
            if ctx.subcommand_passed is None:
                await ctx.send("The following categories we have is:\n- normal\n- ranked\n- whitelist\nTo use the command, do the following ``!vfilter add <category> <word>``")
    
    @filter.command()
    async def review(self, ctx, category: str):
        if category == "ranked":
            message = await ctx.send("Working to fetch the list! This may take a few minutes.")
            pages = Configuration.paginate(", ".join(Configuration.getConfigVar(ctx.guild.id, "RANKED")))
            embed = discord.Embed(title=f"This is {category}'s list of words to keep a eye out on channels other than ranked", description=f"```{pages}```", color=0xff7171)
            await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
        if category == "normal":
            message = await ctx.send("Working to fetch the list! This may take a few minutes.")
            pages = Configuration.paginate(", ".join(Configuration.getConfigVar(ctx.guild.id, "NORMAL")))
            embed = discord.Embed(title=f"This is {category}'s list of words to keep an eye out on channels other than normal", description=f"```{pages}```", color=0xff7171)
            await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
        if category == "whitelist":
            message = await ctx.send("Working to fetch the list! This may take a few minutes.")
            pages = Configuration.paginate(", ".join(Configuration.getConfigVar(ctx.guild.id, "WHITELIST")))
            embed = discord.Embed(title=f"This is {category}'s list of words to keep an eye out for any false positives", description=f"```{pages}```", color=0xff7171)
            await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
        if category == "unsupported":
            message = await ctx.send("Working to fetch the list! This may take a few minutes.")
            pages = Configuration.paginate(", ".join(Configuration.getConfigVar(ctx.guild.id, "UNSUPPORTED")))
            embed = discord.Embed(title=f"This is {category}'s list of words to keep an eye out", description=f"```{pages}```", color=0xff7171)
            await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
        if category == "lookingfor":
            message = await ctx.send("Working to fetch the list! This may take a few minutes.")
            pages = Configuration.paginate(", ".join(Configuration.getConfigVar(ctx.guild.id, "LOOKINGFOR")))
            embed = discord.Embed(title=f"This is {category}'s list of words to keep an eye out", description=f"```{pages}```", color=0xff7171)
            await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
        else:
            return

    @filter.command()
    async def add(self, ctx, category: str, *, word: str):
        #Channel for channel mentioning thingy.
        Mods = discord.utils.get(ctx.guild.roles, id=703063141990400001)
        normalNA= "<#697060120252776478>"
        normalEU = "<#697060525842104330>"
        rankedNA = "<#705974194906726410>"
        rankedEU = "<#705974465212710952>"

        #Assuming that it's some idiot trying to mess up the bot rather than mods.
        if 703063141990400001 not in [role.id for role in ctx.author.roles]:
            return
        else:
            #Normal NA + EU
            if category == "normal":
                blacklist = Configuration.getConfigVar(ctx.guild.id, "NONRANKED")
                if word in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already added to the list for me to keep a eye out in any channel(s) other than {normalNA} and {normalEU}!")
                else: 
                    blacklist.append(word)
                    await ctx.send(f"I have added ``{word}`` to the list for me to keep a eye out in any channel(s) other than {normalNA} and {normalEU}!")
                    Configuration.setConfigVar(ctx.guild.id, "NONRANKED", blacklist)

            #Ranked NA + EU
            if category == "ranked":
                blacklist = Configuration.getConfigVar(ctx.guild.id, "RANKED")
                if word in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already added to the list for me to keep a eye out in any channel(s) other than {rankedNA} and {rankedEU}!")
                else:
                    blacklist.append(word)
                    await ctx.send(f"I have added ``{word}`` to the list for me to keep a eye out in any channel(s) other than {rankedNA} and {rankedEU}!")
                    Configuration.setConfigVar(ctx.guild.id, "RANKED", blacklist)
            
            #Whitelist for any false positives
            if category == "whitelist":
                ignore = Configuration.getConfigVar(ctx.guild.id, "WHITELIST")
                if word in ignore:
                    await ctx.send(f"Looks like that ``{word}`` is already added to the list for me to keep a eye out in {rankedNA} | {rankedEU} and {normalNA} | {normalEU} in case of any false positives.")
                else:
                    ignore.append(word)
                    await ctx.send(f"I have added ``{word}`` to the list for me to keep a eye out in {rankedNA} | {rankedEU} and {normalNA} | {normalEU} in case of any false positives.")
                    Configuration.setConfigVar(ctx.guild.id, "WHITELIST", ignore)
            #Unsupported related things
            if category == "unsupported":
                blacklist = Configuration.getConfigVar(ctx.guild.id, "UNSUPPORTED")
                if word in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already added to the list for me to keep a eye out!")
                else:
                    blacklist.append(word)
                    await ctx.send(f"I have added ``{word}`` to the list for me to keep a eye out!")
                    Configuration.setConfigVar(ctx.guild.id, "UNSUPPORTED", blacklist)
            if category == "lookingfor":
                blacklist = Configuration.getConfigVar(ctx.guild.id, "LOOKINGFOR")
                if word in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already added to the list for me to keep a eye out!")
                else:
                    blacklist.append(word)
                    await ctx.send(f"I have added ``{word}`` to the list for me to keep a eye out!")
                    Configuration.setConfigVar(ctx.guild.id, "LOOKINGFOR", blacklist)
            else:
                await ctx.send("The following categories we have is:\n- normal\n- ranked\n- whitelist\n- unsupported\n- lookingfor\nTo use the command, do the following ``!vfilter add <category> <word>``")
            

    
    @filter.command()
    async def remove(self, ctx, category:str, *, word: str):
        #Channel for channel mentioning thingy.
        Mods = discord.utils.get(ctx.guild.roles, id=703063141990400001)
        normalNA= "<#697060120252776478>"
        normalEU = "<#697060525842104330>"
        rankedNA = "<#705974194906726410>"
        rankedEU = "<#705974465212710952>"

        #Assuming that it's some idiot trying to mess up the bot rather than mods.
        if 703063141990400001 not in [role.id for role in ctx.author.roles]:
            return
        else:
            #Normal NA + EU
            if category == "normal":
                blacklist = Configuration.getConfigVar(ctx.guild.id, "NONRANKED")
                if word not in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already removed from the list and I'm not currently keeping an eye out in any channel(s) other than {normalNA} and {normalEU} for {word}!")
                else: 
                    blacklist.remove(word)
                    await ctx.send(f"I have removed ``{word}`` from the list I will no longer keep an eye out in any channel(s) other than {normalNA} and {normalEU} for {word}!")
                    Configuration.setConfigVar(ctx.guild.id, "NONRANKED", blacklist)

            #Ranked NA + EU
            if category == "ranked":
                blacklist = Configuration.getConfigVar(ctx.guild.id, "RANKED")
                if word not in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already removed from the list and I'm not currently keeping an eye out in any channel(s) other than {rankedNA} and {rankedEU} for {word}!")
                else:
                    blacklist.remove(word)
                    await ctx.send(f"I have removed ``{word}`` to the list I will no longer keep an eye out in any channel(s) other than {rankedNA} and {rankedEU} for {word}!")
                    Configuration.setConfigVar(ctx.guild.id, "RANKED", blacklist)
            
            #Whitelist for any false positives
            if category == "whitelist":
                ignore = Configuration.getConfigVar(ctx.guild.id, "WHITELIST")
                if word not in ignore:
                    await ctx.send(f"Looks like that ``{word}`` has been removed from the list for me to keep a eye out in {rankedNA} | {rankedEU} and {normalNA} | {normalEU} in case of any false positives.")
                else:
                    ignore.remove(word)
                    await ctx.send(f"I have removed ``{word}`` from the list for me to keep a eye out in {rankedNA} | {rankedEU} and {normalNA} | {normalEU} in case of any false positives. I will no longer keep a eye out for {word}")
                    Configuration.setConfigVar(ctx.guild.id, "WHITELIST", ignore)

            #Unsupported related things
            if category == "unsupported":
                blacklist = Configuration.getConfigVar(ctx.guild.id, "UNSUPPORTED")
                if word not in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already removed from the list and I'm not currently keeping an eye out in any channels for {word}.")
                else:
                    blacklist.remove(word)
                    await ctx.send(f"I have removed ``{word}`` to the list I will no longer keep an eye out in any channels for {word}.")
                    Configuration.setConfigVar(ctx.guild.id, "UNSUPPORTED", blacklist)
            if category == "lookingfor":
                blacklist = Configuration.getConfigVar(ctx.guild.id, "LOOOKINGFOR")
                if word not in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already removed from the list and I'm not currently keeping an eye out in any channels for {word}.")
                else:
                    blacklist.remove(word)
                    await ctx.send(f"I have removed ``{word}`` to the list I will no longer keep an eye out in any channels for {word}.")
                    Configuration.setConfigVar(ctx.guild.id, "LOOKING FOR", blacklist)
            else:
                await ctx.send("The following categories we have is:\n- normal\n- ranked\n- whitelist\n- unsupported\n- lookingfor\nTo use the command, do the following ``!vfilter remove <category> <word>``")
    
    @commands.Cog.listener()
    async def on_connect(self):
        log = self.bot.get_channel(712640778136059975)
        embed = discord.Embed(title=f"Connected to the gateway.", description=f"Connected to the gateway.", color=5109096)
        await log.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_disconnect(self):
        log = self.bot.get_channel(712640778136059975)
        embed = discord.Embed(title=f"Disconnected from the gateway.", description=f"Disconnected from the gateway.", color=16098851)
        await log.send(embed=embed)    
    
    @commands.Cog.listener()
    async def on_resume(self):
        log = self.bot.get_channel(712640778136059975)
        embed = discord.Embed(title=f"Resumed connection to the gateway", description=f"Must be the bot, not Discord xd", color=16098851)
        await log.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        #Channel for channel mentioning thingy.
        normalNA= "<#697060120252776478>"
        normalEU = "<#697060525842104330>"
        rankedNA = "<#705974194906726410>"
        rankedEU = "<#705974465212710952>"
        modmail = "<@703058322944950394>"

        #looking for normal NA
        if message.channel.id == 697060120252776478:
            if message.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in message.author.roles]:
                return
            if 684144438251225099 in [role.id for role in message.author.roles]:
                return
            else:
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                whitelist = Configuration.getConfigVar(message.guild.id, "WHITELIST")
                if any(word in message.content.lower() for word in whitelist):
                    return
                if any(word in message.content.lower() for word in unsupported):
                    response = await message.channel.send(f"Hey there {message.author.mention}, I'm afraid that we don't support any type of tournaments or recruiting in our Looking For.\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                    log = self.bot.get_channel(683067565127237705)
                    embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {message.author.name}#{message.author.discriminator} (``{message.author.id}``) in {message.channel.mention} containing:\n\n```{message.content}```", color=0xff7171)
                    await log.send(embed=embed)
                    await asyncio.sleep(15)
                    await message.delete()
                    await response.delete()
                else:
                    ranking = Configuration.getConfigVar(message.guild.id, "RANKED")
                    if any(word in message.content.lower() for word in ranking):
                            response = await message.channel.send(f"Hey there {message.author.mention}, I believe you may be looking for this channel :arrow_right: **{rankedNA}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                            log = self.bot.get_channel(683067565127237705)
                            embed = discord.Embed(title=f"Filtered Word from Ranked Category", description=f"Found message from {message.author.name}#{message.author.discriminator} (``{message.author.id}``) in {message.channel.mention} containing:\n\n```{message.content}```", color=0xff7171)
                            await log.send(embed=embed)
                            await asyncio.sleep(15)
                            await message.delete()
                            await response.delete()
                    else:
                        return
        if message.guild.id == 679875946597056683:
            if message.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in message.author.roles]:
                return
            if 684144438251225099 in [role.id for role in message.author.roles]:
                return
            else:
                lookingfor = Configuration.getConfigVar(message.guild.id, "LOOKINGFOR")
                if any(word in message.content.lower() for word in lookingfor):
                    log = self.bot.get_channel(683067565127237705)
                    embed = discord.Embed(title=f"Filtered Word that was looking for group", description=f"Found message from {message.author.name}#{message.author.discriminator} (``{message.author.id}``) in {message.channel.mention} containing:\n\n```{message.content}```", color=0xff7171)
                    await log.send(embed=embed)
                    await message.delete()

        #looking for normal EU
        if message.channel.id == 697060525842104330: 
            if message.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in message.author.roles]:
                return
            if 684144438251225099 in [role.id for role in message.author.roles]:
                return
            else:
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                whitelist = Configuration.getConfigVar(message.guild.id, "WHITELIST")
                if any(word in message.content.lower() for word in whitelist):
                    return
                if any(word in message.content.lower() for word in unsupported):
                    response = await message.channel.send(f"Hey there {message.author.mention}, I'm afraid that we don't support any type of tournaments or recruiting in our Looking For.\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                    log = self.bot.get_channel(683067565127237705)
                    embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {message.author.name}#{message.author.discriminator} (``{message.author.id}``) in {message.channel.mention} containing:\n\n```{message.content}```", color=0xff7171)
                    await log.send(embed=embed)
                    asyncio.sleep(15)
                    await message.delete()
                    await response.delete()
                else:
                    ranking = Configuration.getConfigVar(message.guild.id, "RANKED")
                    if any(word in message.content.lower() for word in ranking):
                            response = await message.channel.send(f"Hey there {message.author.mention}, seems like you may be looking for this channel :arrow_right: **{rankedEU}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                            log = self.bot.get_channel(683067565127237705)
                            embed = discord.Embed(title=f"Filtered Word from Ranked Category", description=f"Found message from {message.author.name}#{message.author.discriminator} (``{message.author.id}``) in {message.channel.mention} containing:\n\n{message.content}", color=0xff7171)
                            await log.send(embed=embed)
                            await asyncio.sleep(15)
                            await message.delete()
                            await response.delete()
                    else:
                        return
    
        #looking for ranked NA
        if message.channel.id == 705974194906726410:
            if message.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in message.author.roles]:
                return
            if 684144438251225099 in [role.id for role in message.author.roles]:
                return
            else:
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                whitelist = Configuration.getConfigVar(message.guild.id, "WHITELIST")
                if any(word in message.content.lower() for word in whitelist):
                    return
                if any(word in message.content.lower() for word in unsupported):
                    response = await message.channel.send(f"Hey there {message.author.mention}, I'm afraid that we don't support any type of tournaments or recruiting in our Looking For.\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                    log = self.bot.get_channel(683067565127237705)
                    embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {message.author.name}#{message.author.discriminator} (``{message.author.id}``) in {message.channel.mention} containing:\n\n```{message.content}```", color=0xff7171)
                    await log.send(embed=embed)
                    await asyncio.sleep(15)
                    await message.delete()
                    await response.delete()
                else:
                    ranking = Configuration.getConfigVar(message.guild.id, "NONRANKED")
                    if any(word in message.content.lower() for word in ranking):
                            response = await message.channel.send(f"{message.author.mention}, seems like you may be looking for this channel :arrow_right: **{normalNA}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                            log = self.bot.get_channel(683067565127237705)
                            embed = discord.Embed(title=f"Filtered Word from non-ranked Category", description=f"Found message from {message.author.name}#{message.author.discriminator} (``{message.author.id}``) in {message.channel.mention} containing:\n\n```{message.content}```", color=0xff7171)
                            await log.send(embed=embed)
                            await asyncio.sleep(15)
                            await message.delete()
                            await response.delete()
                    else:
                        return

        #looking for ranked EU
        if message.channel.id == 705974465212710952:
            if message.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in message.author.roles]:
                return
            if 684144438251225099 in [role.id for role in message.author.roles]:
                return
            else:
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                whitelist = Configuration.getConfigVar(message.guild.id, "WHITELIST")
                if any(word in message.content.lower() for word in whitelist):
                    return
                if any(word in message.content.lower() for word in unsupported):
                    response = await message.channel.send(f"Hey there {message.author.mention}, I'm afraid that we don't support any type of tournaments or recruiting in our Looking For.\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                    log = self.bot.get_channel(683067565127237705)
                    embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {message.author.name}#{message.author.discriminator} (``{message.author.id}``) in {message.channel.mention} containing:\n\n```{message.content}```", color=0xff7171)
                    await log.send(embed=embed)
                    await asyncio.sleep(15)
                    await message.delete()
                    await response.delete()
                else:
                    ranking = Configuration.getConfigVar(message.guild.id, "NONRANKED")
                    if any(word in message.content.lower() for word in ranking):
                            response = await message.channel.send(f"{message.author.mention}, seems like you may be looking for this channel :arrow_right: **{normalEU}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                            log = self.bot.get_channel(683067565127237705)
                            embed = discord.Embed(title=f"Filtered Word from non-ranked Category", description=f"Found message from {message.author.name}#{message.author.discriminator} (``{message.author.id}``) in {message.channel.mention} containing:\n\n```{message.content}```", color=0xff7171)
                            await log.send(embed=embed)
                            await asyncio.sleep(15)
                            await message.delete()
                            await response.delete()
                    else:
                        return
        else:
            return


def setup(bot):
    bot.add_cog(main(bot))
