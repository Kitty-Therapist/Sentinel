import asyncio
import datetime
import discord
import configparser
import os
import time
import traceback
import logging
import shlex

from discord.ext import commands
from discord.ext.commands import BucketType
from discord import abc
from discord.abc import PrivateChannel
from discord.utils import get
from utils import Util, Configuration
from argparse import ArgumentParser

class lookingfor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #@commands.command()
    #@commands.guild_only()
    #async def votekick(self, ctx:commands.Context, member: discord.Member, *, reason=""):
    #    reaction = ["👍"]
    #    if ctx.author.voice:
    #        if ctx.guild.get_member(member.id) is None:
    #            embed=discord.Embed(title="Unknown Member Error", description=f":warning: I was not able to start a votekick for {member.name}#{member.discriminator} (``{member.id}``). It seems like they likely left this server or was kicked by a moderator.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
    #            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
    #            return await ctx.send(embed=embed)
    #        if reason is None:
    #            embed=discord.Embed(title="Votekick Reason Required", description=f":warning: You are required to supply a reason of why you would like to votekick {member.name}#{member.discriminator} (``{member.id}``). Please provide a reason and try again.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
    #            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
    #            await ctx.send(embed=embed)
    #        if member.id == ctx.author.id:
    #            embed=discord.Embed(title="Nice try, gamer.", description=f":warning: Sorry, you cannot vote-kick yourself. If you really wanted to leave the voice channel, there is a disconnect button.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
    #            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
    #            await ctx.send(embed=embed)
    #        else:
    #            connected_users = []
    #            for user in ctx.author.voice.channel.members:
    #                connected_users.append("{} ({})".format(str(user), user.id))
    #            users = ("\n".join(connected_users))
    #            embed=discord.Embed(title="Votekick Pending", description=f"{ctx.author.name}#{ctx.author.discriminator} (``{ctx.author.id}``) would like to kick {member.name}#{member.discriminator} (``{member.id}``) for the following reason: {reason}. \n\nIf you agree with the kick, please react below to register your vote.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
    #            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
    #            m = await ctx.send(embed=embed)
    #            for name in reaction:
    #                emoji = get(ctx.guild.emojis, name=name)
    #                await m.add_reaction(name)
    #    else:
    #        embed=discord.Embed(title="Not in Voice Channel", description=f":warning: I was not able to process the votekick as you are not in the Voice Channel!", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
    #        embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
    #        return await ctx.send(embed=embed)


    @commands.group()
    async def filter(self, ctx:commands.Context):
        """Base commands for the filtered related word list."""
        modrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "MODROLE"))
        if modrole not in ctx.author.roles:
            return
        else:
            if ctx.subcommand_passed is None:
                await ctx.send("The following categories we have are:\n- normal\n- ranked\n- unsupported\nTo use the command, do the following ``>filter add <category> <word>``")
    
    @filter.command()
    async def review(self, ctx, category: str):
        modrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "MODROLE"))
        if modrole not in ctx.author.roles:
            return
        if category == "ranked":
            message = await ctx.send("Working to fetch the list! This may take a few minutes.")
            pages = Configuration.paginate(", ".join(Configuration.getConfigVar(ctx.guild.id, "RANKED")))
            embed = discord.Embed(title=f"This is {category}'s list of words to keep a eye out on channels other than ranked", description=f"```{pages}```", color=0xff7171)
            await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
        if category == "normal":
            message = await ctx.send("Working to fetch the list! This may take a few minutes.")
            pages = Configuration.paginate(", ".join(Configuration.getConfigVar(ctx.guild.id, "NONRANKED")))
            embed = discord.Embed(title=f"This is {category}'s list of words to keep an eye out on channels other than normal", description=f"```{pages}```", color=0xff7171)
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
        #Assuming that it's some idiot trying to mess up the bot rather than mods.
        modrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "MODROLE"))
        normalNA = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "NONRANKED-NA"))
        rankedNA = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "RANKED-NA"))
        normalEU = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "NONRANKED-EU"))
        rankedEU = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "RANKED-EU"))
        normalOther = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "NONRANKED-OTHER"))
        rankedOther = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "RANKED-OTHER"))
        if modrole not in ctx.author.roles:
            return
        else:
            #Normal NA + EU
            if category == "normal":
                blacklist = Configuration.getConfigVar(ctx.guild.id, "NONRANKED")
                if word in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already added to the list for me to keep a eye out in any channel(s) other than {normalNA.mention}, {normalEU.mention}, and {normalOther.mention}!")
                else: 
                    blacklist.append(word)
                    await ctx.send(f"I have added ``{word}`` to the list for me to keep a eye out in any channel(s) other than {normalNA.mention}, {normalEU.mention}, and {normalOther.mention}!")
                    Configuration.setConfigVar(ctx.guild.id, "NONRANKED", blacklist)

            #Ranked NA + EU
            if category == "ranked":
                blacklist = Configuration.getConfigVar(ctx.guild.id, "RANKED")
                if word in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already added to the list for me to keep a eye out in any channel(s) other than {rankedNA.mention}, {rankedEU.mention}, and {rankedOther.mention}!")
                else:
                    blacklist.append(word)
                    await ctx.send(f"I have added ``{word}`` to the list for me to keep a eye out in any channel(s) other than {rankedNA.mention}, {rankedEU.mention}, and {rankedOther.mention}!")
                    Configuration.setConfigVar(ctx.guild.id, "RANKED", blacklist)
            
            #Unsupported related things
            if category == "unsupported":
                blacklist = Configuration.getConfigVar(ctx.guild.id, "UNSUPPORTED")
                if word in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already added to the list for me to keep a eye out!")
                else:
                    blacklist.append(word)
                    await ctx.send(f"I have added ``{word}`` to the list for me to keep a eye out!")
                    Configuration.setConfigVar(ctx.guild.id, "UNSUPPORTED", blacklist)

    
    @filter.command()
    async def remove(self, ctx, category:str, *, word: str):
        #Assuming that it's some idiot trying to mess up the bot rather than mods.
        modrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "MODROLE"))
        normalNA = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "NONRANKED-NA"))
        rankedNA = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "RANKED-NA"))
        normalEU = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "NONRANKED-EU"))
        rankedEU = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "RANKED-EU"))
        normalOther = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "NONRANKED-OTHER"))
        rankedOther = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "RANKED-OTHER"))
        if modrole not in ctx.author.roles:
            return
        else:
            #Normal NA + EU
            if category == "normal":
                blacklist = Configuration.getConfigVar(ctx.guild.id, "NONRANKED")
                if word not in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already removed from the list and I'm not currently keeping an eye out in any channel(s) other than {normalNA}, {normalEU}, and {normalOther} for {word}!")
                else: 
                    blacklist.remove(word)
                    await ctx.send(f"I have removed ``{word}`` from the list I will no longer keep an eye out in any channel(s) other than {normalNA}, {normalEU}, and {normalOther} for {word}!")
                    Configuration.setConfigVar(ctx.guild.id, "NONRANKED", blacklist)

            #Ranked NA + EU
            if category == "ranked":
                blacklist = Configuration.getConfigVar(ctx.guild.id, "RANKED")
                if word not in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already removed from the list and I'm not currently keeping an eye out in any channel(s) other than {rankedNA}, {rankedEU}, and {rankedOther} for {word}!")
                else:
                    blacklist.remove(word)
                    await ctx.send(f"I have removed ``{word}`` to the list I will no longer keep an eye out in any channel(s) other than {rankedNA}, {rankedEU}, and {rankedOther} for {word}!")
                    Configuration.setConfigVar(ctx.guild.id, "RANKED", blacklist)

            #Unsupported related things
            if category == "unsupported":
                blacklist = Configuration.getConfigVar(ctx.guild.id, "UNSUPPORTED")
                if word not in blacklist:
                    await ctx.send(f"Looks like that ``{word}`` is already removed from the list and I'm not currently keeping an eye out in any channels for {word}.")
                else:
                    blacklist.remove(word)
                    await ctx.send(f"I have removed ``{word}`` to the list I will no longer keep an eye out in any channels for {word}.")
                    Configuration.setConfigVar(ctx.guild.id, "UNSUPPORTED", blacklist)

    ##This is for the on message events. Some things are hard-coded and I need to look into this.

    @commands.Cog.listener()
    async def on_message(self, message):
        #Channel for channel mentioning thingy.
        normalNA = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "NONRANKED-NA"))
        rankedNA = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "RANKED-NA"))
        normalEU = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "NONRANKED-EU"))
        rankedEU = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "RANKED-EU"))
        normalOther = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "NONRANKED-OTHER"))
        rankedOther = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "RANKED-OTHER"))
        logging = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "LOGGING"))
        modmail = "<@711678018573303809>"
        

        #looking for normal NA
        if message.channel.id == normalNA.id:
            if message.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in message.author.roles]:
                return
            if 684144438251225099 in [role.id for role in message.author.roles]:
                return
            else:
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                ranking = Configuration.getConfigVar(message.guild.id, "RANKED")
                split = shlex.split(message.content.lower())
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await message.channel.send(f"Hey there {message.author.mention}, I'm afraid that we don't support any type of tournaments, recruiting, or fast forfeit in our Looking For.\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(embed=embed)
                        await asyncio.sleep(15)
                        await message.delete()
                        await response.delete()
                for word in (w.lower() for w in ranking):
                    if word in split:
                        response = await message.channel.send(f"Hey there {message.author.mention}, I believe you may be looking for this channel :arrow_right: **{rankedNA.mention}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Ranked Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(embed=embed)
                        await asyncio.sleep(15)
                        await message.delete()
                        await response.delete()
                else:
                    return

        #looking for normal EU
        if message.channel.id == normalEU.id: 
            if message.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in message.author.roles]:
                return
            if 684144438251225099 in [role.id for role in message.author.roles]:
                return
            else:
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                ranking = Configuration.getConfigVar(message.guild.id, "RANKED")
                split = shlex.split(message.content.lower())
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await message.channel.send(f"Hey there {message.author.mention}, I'm afraid that we don't support any type of tournaments, recruiting, or fast forfeit in our Looking For.\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(embed=embed)
                        await asyncio.sleep(15)
                        await message.delete()
                        await response.delete()
                for word in (w.lower() for w in ranking):
                    if word in split:
                        response = await message.channel.send(f"Hey there {message.author.mention}, I believe you may be looking for this channel :arrow_right: **{rankedEU.mention}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Ranked Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(embed=embed)
                        await asyncio.sleep(15)
                        await message.delete()
                        await response.delete()
                else:
                    return
    
        #looking for ranked NA
        if message.channel.id == rankedNA.id:
            if message.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in message.author.roles]:
                return
            if 684144438251225099 in [role.id for role in message.author.roles]:
                return
            else:
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                ranking = Configuration.getConfigVar(message.guild.id, "NONRANKED")
                split = shlex.split(message.content.lower())
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await message.channel.send(f"Hey there {message.author.mention}, I'm afraid that we don't support any type of tournaments, recruiting, or fast forfeit in our Looking For.\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(embed=embed)
                        await asyncio.sleep(15)
                        await message.delete()
                        await response.delete()
                for word in (w.lower() for w in ranking):
                    if word in split:
                        response = await message.channel.send(f"Hey there {message.author.mention}, I believe you may be looking for this channel :arrow_right: **{normalNA.mention}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Unranked Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(embed=embed)
                        await asyncio.sleep(15)
                        await message.delete()
                        await response.delete()
                else:
                    return

        #looking for ranked EU
        if message.channel.id == rankedEU.id:
            if message.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in message.author.roles]:
                return
            if 684144438251225099 in [role.id for role in message.author.roles]:
                return
            else:
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                ranking = Configuration.getConfigVar(message.guild.id, "NONRANKED")
                split = shlex.split(message.content.lower())
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await message.channel.send(f"Hey there {message.author.mention}, I'm afraid that we don't support any type of tournaments, recruiting, or fast forfeit in our Looking For.\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(embed=embed)
                        await asyncio.sleep(15)
                        await message.delete()
                        await response.delete()
                for word in (w.lower() for w in ranking):
                    if word in split:
                        response = await message.channel.send(f"Hey there {message.author.mention}, I believe you may be looking for this channel :arrow_right: **{normalEU.mention}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Unranked Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(embed=embed)
                        await asyncio.sleep(15)
                        await message.delete()
                        await response.delete()
                else:
                    return

        #looking for normal Other
        if message.channel.id == normalOther.id:
            if message.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in message.author.roles]:
                return
            if 684144438251225099 in [role.id for role in message.author.roles]:
                return
            else:
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                ranking = Configuration.getConfigVar(message.guild.id, "RANKED")
                split = shlex.split(message.content.lower())
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await message.channel.send(f"Hey there {message.author.mention}, I'm afraid that we don't support any type of tournaments, recruiting, or fast forfeit in our Looking For.\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(embed=embed)
                        await asyncio.sleep(15)
                        await message.delete()
                        await response.delete()
                for word in (w.lower() for w in ranking):
                    if word in split:
                        response = await message.channel.send(f"Hey there {message.author.mention}, I believe you may be looking for this channel :arrow_right: **{rankedOther.mention}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Ranked Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **word**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(embed=embed)
                        await asyncio.sleep(15)
                        await message.delete()
                        await response.delete()
                else:
                    return

        if message.author.id == 706269652724219987:
            return
        if 679879783630372865 in [role.id for role in message.author.roles]:
            return
        if 684144438251225099 in [role.id for role in message.author.roles]:
            return
        if 703063141990400001 in [role.id for role in message.author.roles]:
            return
        if 695765776086597663 in [role.id for role in message.author.roles]:
            return
        else:
            split = shlex.split(message.content.lower())
            censor = Configuration.getConfigVar(message.guild.id, "CENSOR")
            for word in (w.lower() for w in censor):
                if word in split:
                    response = await message.channel.send(f"Do not send any inappropriate language or non-permitted domains.")
                    logging = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "LOGGING"))
                    embed = discord.Embed(title=f"Filtered Message in Censor", description=f"Found message from {message.author.name}#{message.author.discriminator} (``{message.author.id}``) in {message.channel.mention} containing:\n\n```{message.content}```", color=0xff7171)
                    await logging.send(embed=embed)
                    asyncio.sleep(15)
                    await message.delete()
                    await response.delete()
        #looking for ranked Other
        if message.channel.id == rankedOther.id:
            if message.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in message.author.roles]:
                return
            if 684144438251225099 in [role.id for role in message.author.roles]:
                return
            else:
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                ranking = Configuration.getConfigVar(message.guild.id, "UNRANKED")
                split = shlex.split(message.content.lower())
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await message.channel.send(f"Hey there {message.author.mention}, I'm afraid that we don't support any type of tournaments, recruiting, or fast forfeit in our Looking For.\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(embed=embed)
                        await asyncio.sleep(15)
                        await message.delete()
                        await response.delete()
                for word in (w.lower() for w in ranking):
                    if word in split:
                        response = await message.channel.send(f"Hey there {message.author.mention}, I believe you may be looking for this channel :arrow_right: **{normalOther.mention}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Unranked Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(embed=embed)
                        await asyncio.sleep(15)
                        await message.delete()
                        await response.delete()
                else:
                    return
           
        

def setup(bot):
    bot.add_cog(lookingfor(bot))
