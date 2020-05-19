import discord
import asyncio
import os
import subprocess
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
    async def update(self, ctx):
        """Pulls the latest changes from git."""
        # TODO: This is blocking code :( Needs to be fixed.
        if ctx.author.id == 298618155281154058:
            process = subprocess.Popen(git.split(), stdout=subprocess.PIPE)
            out, err = process.communicate()
            await ctx.send(f"Fetched latest changes from git: ```diff\n{out}\n```")
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
            embed = discord.Embed(title=f"This is{category}'s list of words to keep an eye out on channels other than normal", description=f"```{pages}```", color=0xff7171)
            await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
        if category == "whitelist":
            message = await ctx.send("Working to fetch the list! This may take a few minutes.")
            pages = Configuration.paginate(", ".join(Configuration.getConfigVar(ctx.guild.id, "WHITELIST")))
            embed = discord.Embed(title=f"This is{category}'s list of words to keep an eye out for any false positives", description=f"```{pages}```", color=0xff7171)
            await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
        if category == "unsupported":
            message = await ctx.send("Working to fetch the list! This may take a few minutes.")
            pages = Configuration.paginate(", ".join(Configuration.getConfigVar(ctx.guild.id, "UNSUPPORTED")))
            embed = discord.Embed(title=f"This is{category}'s list of words to keep an eye out", description=f"```{pages}```", color=0xff7171)
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
            else:
                await ctx.send("The following categories we have is:\n- normal\n- ranked\n- whitelist\n- unsupported\nTo use the command, do the following ``!vfilter add <category> <word>``")
    
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
                if word in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already removed from the list and I'm not currently keeping an eye out in any channel(s) other than {normalNA} and {normalEU} for {word}!")
                else: 
                    blacklist.remove(word)
                    await ctx.send(f"I have removed ``{word}`` from the list I will no longer keep an eye out in any channel(s) other than {normalNA} and {normalEU} for {word}!")
                    Configuration.setConfigVar(ctx.guild.id, "NONRANKED", blacklist)

            #Ranked NA + EU
            if category == "ranked":
                blacklist = Configuration.getConfigVar(ctx.guild.id, "RANKED")
                if word in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already removed from the list and I'm not currently keeping an eye out in any channel(s) other than {rankedNA} and {rankedEU} for {word}!")
                else:
                    blacklist.remove(word)
                    await ctx.send(f"I have removed ``{word}`` to the list I will no longer keep an eye out in any channel(s) other than {rankedNA} and {rankedEU} for {word}!")
                    Configuration.setConfigVar(ctx.guild.id, "RANKED", blacklist)
            
            #Whitelist for any false positives
            if category == "whitelist":
                ignore = Configuration.getConfigVar(ctx.guild.id, "WHITELIST")
                if word in ignore:
                    await ctx.send(f"Looks like that ``{word}`` has been removed from the list for me to keep a eye out in {rankedNA} | {rankedEU} and {normalNA} | {normalEU} in case of any false positives.")
                else:
                    ignore.remove(word)
                    await ctx.send(f"I have removed ``{word}`` from the list for me to keep a eye out in {rankedNA} | {rankedEU} and {normalNA} | {normalEU} in case of any false positives. I will no longer keep a eye out for {word}")
                    Configuration.setConfigVar(ctx.guild.id, "WHITELIST", ignore)

            #Unsupported related things
            if category == "unsupported":
                blacklist = Configuration.getConfigVar(ctx.guild.id, "UNSUPPORTED")
                if word in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already removed from the list and I'm not currently keeping an eye out in any channels for {word}.")
                else:
                    blacklist.remove(word)
                    await ctx.send(f"I have removed ``{word}`` to the list I will no longer keep an eye out in any channels for {word}.")
                    Configuration.setConfigVar(ctx.guild.id, "UNSUPPORTED", blacklist)
            else:
                await ctx.send("The following categories we have is:\n- normal\n- ranked\n- whitelist\n- unsupported\nTo use the command, do the following ``!vfilter remove <category> <word>``")

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
            else:
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                whitelist = Configuration.getConfigVar(message.guild.id, "WHITELIST")
                if any(word in message.content.lower() for word in whitelist):
                    return
                elif any(word in message.content.lower() for word in unsupported):
                    response = await message.channel.send(f"Hey there {message.author.mention}, I'm afraid that we don't support any type of tournaments or recruiting in our Looking For.\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                    await asyncio.sleep(15)
                    await message.delete()
                    await response.delete()
                    return
                else:
                    ranking = Configuration.getConfigVar(message.guild.id, "RANKED")
                    if any(word in message.content.lower() for word in ranking):
                            response = await message.channel.send(f"Hey there {message.author.mention}, I believe you may be looking for this channel :arrow_right: **{rankedNA}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                            await asyncio.sleep(15)
                            await message.delete()
                            await response.delete()
                    else:
                        return
        else:
            return

        #looking for normal EU
        if message.channel.id == 697060525842104330:
            if message.author.id == 706269652724219987:
                return
            else:
                whitelist = Configuration.getConfigVar(message.guild.id, "WHITELIST")
                if any(word in message.content.lower() for word in whitelist):
                    return
                elif any(word in message.content.lower() for word in unsupported):
                    response = await message.channel.send(f"Hey there {message.author.mention}, I'm afraid that we don't support any type of tournaments or recruiting in our Looking For.\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                    asyncio.sleep(15)
                    await message.delete()
                    await response.delete()
                    return
                else:
                    ranking = Configuration.getConfigVar(message.guild.id, "RANKED")
                    if any(word in message.content.lower() for word in ranking):
                            response = await message.channel.send(f"Hey there {message.author.mention}, seems like you may be looking for this channel :arrow_right: **{rankedEU}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                            await asyncio.sleep(15)
                            await message.delete()
                            await response.delete()
                    else:
                        return
        else:
            return
    
            #looking for ranked NA
        if message.channel.id == 705974194906726410:
            if message.author.id == 706269652724219987:
                return
            else:
                whitelist = Configuration.getConfigVar(message.guild.id, "WHITELIST")
                if any(word in message.content.lower() for word in whitelist):
                    return
                elif any(word in message.content.lower() for word in unsupported):
                    response = await message.channel.send(f"Hey there {message.author.mention}, I'm afraid that we don't support any type of tournaments or recruiting in our Looking For.\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                    await asyncio.sleep(15)
                    await message.delete()
                    await response.delete()
                    return
                else:
                    ranking = Configuration.getConfigVar(message.guild.id, "NONRANKED")
                    if any(word in message.content.lower() for word in ranking):
                            response = await message.channel.send(f"{message.author.mention}, seems like you may be looking for this channel :arrow_right: **{normalNA}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                            await asyncio.sleep(15)
                            await message.delete()
                            await response.delete()
                    else:
                        return
        else:
            return

        #looking for ranked EU
        if message.channel.id == 705974465212710952:
            if message.author.id == 706269652724219987:
                return
            else:
                whitelist = Configuration.getConfigVar(message.guild.id, "WHITELIST")
                if any(word in message.content.lower() for word in whitelist):
                    return
                elif any(word in message.content.lower() for word in unsupported):
                    response = await message.channel.send(f"Hey there {message.author.mention}, I'm afraid that we don't support any type of tournaments or recruiting in our Looking For.\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                    await asyncio.sleep(15)
                    await message.delete()
                    await response.delete()
                    return
                else:
                    ranking = Configuration.getConfigVar(message.guild.id, "NONRANKED")
                    if any(word in message.content.lower() for word in ranking):
                            response = await message.channel.send(f"{message.author.mention}, seems like you may be looking for this channel :arrow_right: **{normalEU}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                            await asyncio.sleep(15)
                            await message.delete()
                            await response.delete()
                    else:
                        return
        else:
            return


def setup(bot):
    bot.add_cog(main(bot))
