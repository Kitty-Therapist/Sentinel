import asyncio
import datetime
import discord
import configparser
import os
import time
import traceback
import logging
import shlex
import re

from discord.ext import commands
from discord.ext.commands import BucketType
from discord import abc, NotFound
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
    @commands.has_permissions(manage_roles=True)
    async def filter(self, ctx:commands.Context):
        """Base commands for the filtered related word list."""
        modrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "MODROLE"))
        adminrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "ADMINROLE"))
        roles = [modrole, adminrole]
        user_roles = [role.id for role in ctx.author.roles]

        else:
            if ctx.subcommand_passed is None:
                await ctx.send("The following categories we have are:\n- normal\n- ranked\n- unsupported\nTo use the command, do the following ``>filter add <category> <word>``")
    
    @filter.command()
    async def review(self, ctx, category: str):
        def split_list(alist, wanted_parts=1):
            length = len(alist)
            return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
                    for i in range(wanted_parts) ]


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
            q1,q2 = split_list(pages, wanted_parts=2)
            embed = discord.Embed(title=f"This is {category}'s list of words to keep an eye out", description=f"```{q1}```", color=0xff7171)
            await ctx.send(embed=embed)
            embed2 = discord.Embed(title=f"This is {category}'s list of words to keep an eye out", description=f"```{q2}```", color=0xff7171)
            await ctx.send(embed=embed2)
            await asyncio.sleep(5)
            await message.delete()
        if category == "lookingforteam":
            message = await ctx.send("Working to fetch the list! This may take a few minutes.")
            pages = Configuration.paginate(", ".join(Configuration.getConfigVar(ctx.guild.id, "LOOKINGFORTEAM")))
            embed = discord.Embed(title=f"This is {category}'s list of words to keep an eye out", description=f"```{pages}```", color=0xff7171)
            await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
        if category == "lookingforplayer":
            message = await ctx.send("Working to fetch the list! This may take a few minutes.")
            pages = Configuration.paginate(", ".join(Configuration.getConfigVar(ctx.guild.id, "LOOKINGFORPLAYERS")))
            embed = discord.Embed(title=f"This is {category}'s list of words to keep an eye out", description=f"```{pages}```", color=0xff7171)
            await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
        if category == "scrimna":
            message = await ctx.send("Working to fetch the list! This may take a few minutes.")
            pages = Configuration.paginate(", ".join(Configuration.getConfigVar(ctx.guild.id, "SCRIM-NA")))
            embed = discord.Embed(title=f"This is {category}'s list of words to keep an eye out", description=f"```{pages}```", color=0xff7171)
            await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
        if category == "scrimeu":
            message = await ctx.send("Working to fetch the list! This may take a few minutes.")
            pages = Configuration.paginate(", ".join(Configuration.getConfigVar(ctx.guild.id, "SCRIM-EU")))
            embed = discord.Embed(title=f"This is {category}'s list of words to keep an eye out", description=f"```{pages}```", color=0xff7171)
            await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
        if category == "scrimother":
            message = await ctx.send("Working to fetch the list! This may take a few minutes.")
            pages = Configuration.paginate(", ".join(Configuration.getConfigVar(ctx.guild.id, "SCRIM-OTHER")))
            embed = discord.Embed(title=f"This is {category}'s list of words to keep an eye out", description=f"```{pages}```", color=0xff7171)
            await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
        if category == "phrases":
            message = await ctx.send("Working to fetch the list! This may take a few minutes.")
            pages = Configuration.paginate(", ".join(Configuration.getConfigVar(ctx.guild.id, "PHRASES")))
            q1,q2 = split_list(pages, wanted_parts=2)
            embed = discord.Embed(title=f"This is {category}'s list of words to keep an eye out", description=f"```{q1}```", color=0xff7171)
            await ctx.send(embed=embed)
            embed2 = discord.Embed(title=f"This is {category}'s list of words to keep an eye out", description=f"```{q2}```", color=0xff7171)
            await ctx.send(embed=embed2)
            await asyncio.sleep(5)
            await message.delete()
        else:
            return

    @filter.command()
    async def add(self, ctx, category: str, *, word: str):
        #Assuming that it's some idiot trying to mess up the bot rather than mods.
        normalNA = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "NONRANKED-NA"))
        rankedNA = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "RANKED-NA"))
        normalEU = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "NONRANKED-EU"))
        rankedEU = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "RANKED-EU"))
        normalOther = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "NONRANKED-OTHER"))
        rankedOther = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "RANKED-OTHER"))
        scrimNA = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "SCRIM-NA"))
        scrimEU = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "SCRIM-EU"))
        scrimOther = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "SCRIM-OTHER"))
        lookingfteam = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "TEAMLF"))
        lookingfplayers = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "PLAYERLF"))

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
        
        if category == "lookingforteam":
            blacklist = Configuration.getConfigVar(ctx.guild.id, "LOOKINGFORTEAM")
            if word in blacklist:
                await ctx.send(f"Looks like that ``{word}`` is already added to the list for me to keep a eye out!")
            else:
                blacklist.append(word)
                await ctx.send(f"I have added ``{word}`` to the list for me to keep a eye out!")
                Configuration.setConfigVar(ctx.guild.id, "LOOKINGFORTEAM", blacklist)

        if category == "lookingforplayers":
            blacklist = Configuration.getConfigVar(ctx.guild.id, "LOOKINGFORPLAYERS")
            if word in blacklist:
                await ctx.send(f"Looks like that ``{word}`` is already added to the list for me to keep a eye out!")
            else:
                blacklist.append(word)
                await ctx.send(f"I have added ``{word}`` to the list for me to keep a eye out!")
                Configuration.setConfigVar(ctx.guild.id, "LOOKINGFORPLAYERS", blacklist)

        if category == "scrimna":
            blacklist = Configuration.getConfigVar(ctx.guild.id, "SCRIMNA")
            if word in blacklist:
                await ctx.send(f"Looks like that ``{word}`` is already added to the list for me to keep a eye out!")
            else:
                blacklist.append(word)
                await ctx.send(f"I have added ``{word}`` to the list for me to keep a eye out!")
                Configuration.setConfigVar(ctx.guild.id, "SCRIMNA", blacklist)
        
        if category == "scrimeu":
            blacklist = Configuration.getConfigVar(ctx.guild.id, "SCRIMEU")
            if word in blacklist:
                await ctx.send(f"Looks like that ``{word}`` is already added to the list for me to keep a eye out!")
            else:
                blacklist.append(word)
                await ctx.send(f"I have added ``{word}`` to the list for me to keep a eye out!")
                Configuration.setConfigVar(ctx.guild.id, "SCRIMEU", blacklist)
        
        if category == "scrimother":
            blacklist = Configuration.getConfigVar(ctx.guild.id, "SCRIMOTHER")
            if word in blacklist:
                await ctx.send(f"Looks like that ``{word}`` is already added to the list for me to keep a eye out!")
            else:
                blacklist.append(word)
                await ctx.send(f"I have added ``{word}`` to the list for me to keep a eye out!")
                Configuration.setConfigVar(ctx.guild.id, "SCRIMOTHER", blacklist)         
        
        if category == "phrases":
            blacklist = Configuration.getConfigVar(ctx.guild.id, "PHRASES")
            count = len(word.split())
            if count <= 1:
                await ctx.send("Your phrase needs to be more than one word!")
            else:
                blacklist.append(word)
                await ctx.send(f"I have added ``{word}`` to the list for me to keep a eye out!")
                Configuration.setConfigVar(ctx.guild.id, "PHRASES", blacklist)

    
    @filter.command()
    async def remove(self, ctx, category:str, *, word: str):
        #Assuming that it's some idiot trying to mess up the bot rather than mods.
        normalNA = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "NONRANKED-NA"))
        rankedNA = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "RANKED-NA"))
        normalEU = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "NONRANKED-EU"))
        rankedEU = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "RANKED-EU"))
        normalOther = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "NONRANKED-OTHER"))
        rankedOther = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "RANKED-OTHER"))
        scrimNA = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "SCRIM-NA"))
        scrimEU = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "SCRIM-EU"))
        scrimOther = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "SCRIM-OTHER"))
        lookingfteam = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "TEAMLF"))
        lookingfplayers = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "PLAYERLF"))

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

        if category == "lookingforteam":
            blacklist = Configuration.getConfigVar(ctx.guild.id, "LOOKINGFORTEAM")
            if word not in blacklist:
                await ctx.send(f"Looks like that ``{word}`` is already removed from the list for me to keep a eye out!")
            else:
                blacklist.remove(word)
                await ctx.send(f"I have remove ``{word}`` from the list for me to keep a eye out!")
                Configuration.setConfigVar(ctx.guild.id, "LOOKINGFORTEAM", blacklist)

        if category == "lookingforplayers":
            blacklist = Configuration.getConfigVar(ctx.guild.id, "LOOKINGFORPLAYERS")
            if word not in blacklist:
                await ctx.send(f"Looks like that ``{word}`` is already removed from the list for me to keep a eye out!")
            else:
                blacklist.remove(word)
                await ctx.send(f"I have removed ``{word}`` from the list for me to keep a eye out!")
                Configuration.setConfigVar(ctx.guild.id, "LOOKINGFORPLAYERS", blacklist)

        if category == "scrimna":
            blacklist = Configuration.getConfigVar(ctx.guild.id, "SCRIMNA")
            if word not in blacklist:
                await ctx.send(f"Looks like that ``{word}`` is already removed from the list for me to keep a eye out!")
            else:
                blacklist.remove(word)
                await ctx.send(f"I have removed ``{word}`` from the list for me to keep a eye out!")
                Configuration.setConfigVar(ctx.guild.id, "SCRIMNA", blacklist)
        
        if category == "scrimeu":
            blacklist = Configuration.getConfigVar(ctx.guild.id, "SCRIMEU")
            if word not in blacklist:
                await ctx.send(f"Looks like that ``{word}`` is already removed from the list for me to keep a eye out!")
            else:
                blacklist.remove(word)
                await ctx.send(f"I have removed ``{word}`` from the list for me to keep a eye out!")
                Configuration.setConfigVar(ctx.guild.id, "SCRIMEU", blacklist)
        
        if category == "scrimother":
            blacklist = Configuration.getConfigVar(ctx.guild.id, "SCRIMOTHER")
            if word not in blacklist:
                await ctx.send(f"Looks like that ``{word}`` is already removed from the list for me to keep a eye out!")
            else:
                blacklist.remove(word)
                await ctx.send(f"I have removed ``{word}`` from the list for me to keep a eye out!")
                Configuration.setConfigVar(ctx.guild.id, "SCRIMOTHER", blacklist)   

        if category == "phrases":
            blacklist = Configuration.getConfigVar(ctx.guild.id, "PHRASES")
            count = len(word.split())
            if count <= 1:
                await ctx.send("This is the phrasing filtering, so it should have more than one word.")
            else:
                blacklist.remove(word)
                await ctx.send(f"I have removed ``{word}`` to the list for me to keep a eye out!")
                Configuration.setConfigVar(ctx.guild.id, "PHRASES", blacklist)

    ##This is for the on message events. Some things are hard-coded and I need to look into this.
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        normalNA = after.guild.get_channel(Configuration.getConfigVar(after.guild.id, "NONRANKED-NA"))
        rankedNA = after.guild.get_channel(Configuration.getConfigVar(after.guild.id, "RANKED-NA"))
        normalEU = after.guild.get_channel(Configuration.getConfigVar(after.guild.id, "NONRANKED-EU"))
        rankedEU = after.guild.get_channel(Configuration.getConfigVar(after.guild.id, "RANKED-EU"))
        normalOther = after.guild.get_channel(Configuration.getConfigVar(after.guild.id, "NONRANKED-OTHER"))
        rankedOther = after.guild.get_channel(Configuration.getConfigVar(after.guild.id, "RANKED-OTHER"))
        scrimna = after.guild.get_channel(Configuration.getConfigVar(after.guild.id, "SCRIM-NA"))
        scrimeu = after.guild.get_channel(Configuration.getConfigVar(after.guild.id, "SCRIM-EU"))
        scrimother = after.guild.get_channel(Configuration.getConfigVar(after.guild.id, "SCRIM-OTHER"))
        lookingforteam = after.guild.get_channel(Configuration.getConfigVar(after.guild.id, "TEAMLF"))
        Lookingforplayers = after.guild.get_channel(Configuration.getConfigVar(after.guild.id, "PLAYERLF"))
        logging = after.guild.get_channel(Configuration.getConfigVar(after.guild.id, "LOGGING"))
        modmail = "<@711678018573303809>"
        channelMessage = f"Hey there {after.author.mention}, I'm afraid that we don't support the type of the request that you're attempting to send.\nIf you believe that this may be in error, please contact {modmail} to let us know with the content in case of any false positives."
        loggingtitle = "Filtered Word from Unsupported Category"
        loggingmessage = f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention}:\n\n```{after.content}```\n\n"

        if normalNA is None:
            return
        if rankedNA is None:
            return
        if normalEU is None:
            return
        if rankedEU is None:
            return
        if normalOther is None:
            return
        if rankedOther is None:
            return
        if scrimna is None:
            return
        if scrimeu is None:
            return
        if scrimother is None:
            return
        if lookingforteam is None:
            return
        if lookingforplayers is None:
            return
        
        #looking for normal NA
        if after.channel.id == normalNA.id:
            if after.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in after.author.roles]:
                return
            if 684144438251225099 in [role.id for role in after.author.roles]:
                return
            else:
                unsupported = Configuration.getConfigVar(after.guild.id, "UNSUPPORTED")
                phrases = Configuration.getConfigVar(after.guild.id, "PHRASES")
                ranking = Configuration.getConfigVar(after.guild.id, "RANKED")
                split = shlex.split(after.content.lower())
                if any(word in after.content.lower() for word in phrases):
                    response = await after.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{after.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await after.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                for word in (w.lower() for w in ranking):
                    if word in split:
                        response = await after.channel.send(f"Hey there {after.author.mention}, I believe you may be looking for this channel :arrow_right: **{rankedNA.mention}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Ranked Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                for word in (w.lower() for w in lookingfor):
                    if word in split:
                        response = await after.channel.send(f"Hey there {after.author.mention}, I believe you may be looking for this channel :arrow_right: **{rankedNA.mention}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Ranked Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return

        #looking for normal EU
        if after.channel.id == normalEU.id: 
            if after.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in after.author.roles]:
                return
            if 684144438251225099 in [role.id for role in after.author.roles]:
                return
            else:
                unsupported = Configuration.getConfigVar(after.guild.id, "UNSUPPORTED")
                phrases = Configuration.getConfigVar(after.guild.id, "PHRASES")
                ranking = Configuration.getConfigVar(after.guild.id, "RANKED")
                split = shlex.split(after.content.lower())
                if any(word in after.content.lower() for word in phrases):
                    response = await after.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{after.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await after.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                for word in (w.lower() for w in ranking):
                    if word in split:
                        response = await after.channel.send(f"Hey there {after.author.mention}, I believe you may be looking for this channel :arrow_right: **{rankedEU.mention}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Ranked Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return
    
        #looking for ranked NA
        if after.channel.id == rankedNA.id:
            if after.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in after.author.roles]:
                return
            if 684144438251225099 in [role.id for role in after.author.roles]:
                return
            else:
                unsupported = Configuration.getConfigVar(after.guild.id, "UNSUPPORTED")
                phrases = Configuration.getConfigVar(after.guild.id, "PHRASES")
                ranking = Configuration.getConfigVar(after.guild.id, "RANKED")
                split = shlex.split(after.content.lower())
                if any(word in after.content.lower() for word in phrases):
                    response = await after.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{after.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await after.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                for word in (w.lower() for w in ranking):
                    if word in split:
                        response = await after.channel.send(f"Hey there {after.author.mention}, I believe you may be looking for this channel :arrow_right: **{normalNA.mention}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Unranked Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return

        #looking for ranked EU
        if after.channel.id == rankedEU.id:
            if after.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in after.author.roles]:
                return
            if 684144438251225099 in [role.id for role in after.author.roles]:
                return
            else:
                unsupported = Configuration.getConfigVar(after.guild.id, "UNSUPPORTED")
                phrases = Configuration.getConfigVar(after.guild.id, "PHRASES")
                ranking = Configuration.getConfigVar(after.guild.id, "RANKED")
                split = shlex.split(after.content.lower())
                if any(word in after.content.lower() for word in phrases):
                    response = await after.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{after.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await after.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                for word in (w.lower() for w in ranking):
                    if word in split:
                        response = await after.channel.send(f"Hey there {after.author.mention}, I believe you may be looking for this channel :arrow_right: **{normalEU.mention}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Unranked Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return

        #looking for normal Other
        if after.channel.id == normalOther.id:
            if after.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in after.author.roles]:
                return
            if 684144438251225099 in [role.id for role in after.author.roles]:
                return
            else:
                unsupported = Configuration.getConfigVar(after.guild.id, "UNSUPPORTED")
                phrases = Configuration.getConfigVar(after.guild.id, "PHRASES")
                ranking = Configuration.getConfigVar(after.guild.id, "RANKED")
                split = shlex.split(after.content.lower())
                if any(word in after.content.lower() for word in phrases):
                    response = await after.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{after.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await after.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                for word in (w.lower() for w in ranking):
                    if word in split:
                        response = await after.channel.send(f"Hey there {after.author.mention}, I believe you may be looking for this channel :arrow_right: **{rankedOther.mention}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Ranked Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **word**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return
        
        #looking for ranked Other
        if after.channel.id == rankedOther.id:
            if after.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in after.author.roles]:
                return
            if 684144438251225099 in [role.id for role in after.author.roles]:
                return
            else:
                unsupported = Configuration.getConfigVar(after.guild.id, "UNSUPPORTED")
                phrases = Configuration.getConfigVar(after.guild.id, "PHRASES")
                ranking = Configuration.getConfigVar(after.guild.id, "RANKED")
                split = shlex.split(after.content.lower())
                if any(word in after.content.lower() for word in phrases):
                    response = await after.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{after.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await after.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                for word in (w.lower() for w in ranking):
                    if word in split:
                        response = await after.channel.send(f"Hey there {after.author.mention}, I believe you may be looking for this channel :arrow_right: **{normalOther.mention}** :arrow_left:\nIf you believe that this may be in error, please contact {modmail} to let us know with the message's content in case of any false positives.")
                        embed = discord.Embed(title=f"Filtered Word from Unranked Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return

        #looking for Scrim NA
        if after.channel.id == scrimna.id:
            if after.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in after.author.roles]:
                return
            if 684144438251225099 in [role.id for role in after.author.roles]:
                return
            else:
                scrimNorthAmerica = Configuration.getConfigVar(after.guild.id, "SCRIM-NA")
                phrases = Configuration.getConfigVar(after.guild.id, "PHRASES")
                split = shlex.split(after.content.lower())
                if any(word in after.content.lower() for word in phrases):
                    response = await after.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{after.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in scrimNorthAmerica):
                    if word in split:
                        response = await after.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Scrim NA Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return
        
        #looking for Scrim EU
        if after.channel.id == scrimeu.id:
            if after.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in after.author.roles]:
                return
            if 684144438251225099 in [role.id for role in after.author.roles]:
                return
            else:
                scrimEurope = Configuration.getConfigVar(after.guild.id, "SCRIM-EU")
                phrases = Configuration.getConfigVar(after.guild.id, "PHRASES")
                split = shlex.split(after.content.lower())
                if any(word in after.content.lower() for word in phrases):
                    response = await after.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{after.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in scrimEurope):
                    if word in split:
                        response = await after.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Scrim EU Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return
        
        #looking for Scrim Other
        if after.channel.id == scrimother.id:
            if after.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in after.author.roles]:
                return
            if 684144438251225099 in [role.id for role in after.author.roles]:
                return
            else:
                scrimOtherRegion = Configuration.getConfigVar(after.guild.id, "SCRIM-OTHER")
                phrases = Configuration.getConfigVar(after.guild.id, "PHRASES")
                split = shlex.split(after.content.lower())
                if any(word in after.content.lower() for word in phrases):
                    response = await after.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{after.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in scrimOtherRegion):
                    if word in split:
                        response = await after.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Scrim Other Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return

        #looking for Players
        if after.channel.id == lookingforplayers.id:
            if after.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in after.author.roles]:
                return
            if 684144438251225099 in [role.id for role in after.author.roles]:
                return
            else:
                lfplayers = Configuration.getConfigVar(after.guild.id, "LOOKINGFORPLAYERS")
                phrases = Configuration.getConfigVar(after.guild.id, "PHRASES")
                split = shlex.split(after.content.lower())
                if any(word in after.content.lower() for word in phrases):
                    response = await after.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{after.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in lfplayers):
                    if word in split:
                        response = await after.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Looking for Players Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return
        
        #looking for Team
        if after.channel.id == lookingforteam.id:
            if after.author.id == 706269652724219987:
                return
            if 679879783630372865 in [role.id for role in after.author.roles]:
                return
            if 684144438251225099 in [role.id for role in after.author.roles]:
                return
            else:
                lfteam = Configuration.getConfigVar(after.guild.id, "LOOKINGFORTEAM")
                phrases = Configuration.getConfigVar(after.guild.id, "PHRASES")
                split = shlex.split(after.content.lower())
                if any(word in after.content.lower() for word in phrases):
                    response = await after.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{after.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in lfteam):
                    if word in split:
                        response = await after.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Looking for Team Category", description=f"Found message from {after.author.name}#{after.author.discriminator} ({after.author.mention}) (``{after.author.id}``) in {after.channel.mention} containing blacklisted word **{word}**:\n\n```{after.content}```", color=0xff7171)
                        await logging.send(f"{after.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await after.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return

    @commands.Cog.listener()
    async def on_message(self, message):
        #Channel for channel mentioning thingy.
        normalNA = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "NONRANKED-NA"))
        rankedNA = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "RANKED-NA"))
        normalEU = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "NONRANKED-EU"))
        rankedEU = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "RANKED-EU"))
        normalOther = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "NONRANKED-OTHER"))
        rankedOther = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "RANKED-OTHER"))
        scrimna = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "SCRIM-NA"))
        scrimeu = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "SCRIM-EU"))
        scrimother = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "SCRIM-OTHER"))
        lookingforplayers = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "PLAYERLF"))
        lookingforteam = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "TEAMLF"))
        logging = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "LOGGING"))
        modmail = "<@711678018573303809>"
        channelMessage = f"Hey there {message.author.mention}, I'm afraid that we don't support the type of the request that you're attempting to send.\nIf you believe that this may be in error, please contact {modmail} to let us know with the content in case of any false positives."
        loggingtitle = "Filtered Word from Unsupported Category"
        loggingmessage = f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention}:\n\n```{message.content}```\n\n"

        if normalNA is None:
            print("pog nothing")
            return
        if rankedNA is None:
            print("does this work?")
            return
        if normalEU is None:
            print("wew what about this?")
            return
        if rankedEU is None:
            print("4")
            return
        if normalOther is None:
            print("5")
            return
        if rankedOther is None:
            print("6")
            return
        if scrimna is None:
            print("7")
            return
        if scrimeu is None:
            print("8")
            return
        if scrimother is None:
            print("9")
            return
        if lookingforteam is None:
            print("10")
            return
        if lookingforplayers is None:
            print("11")
            return
        if message.author.id == 706269652724219987:
            return
        if 679879783630372865 in [role.id for role in message.author.roles]:
            return
        if 684144438251225099 in [role.id for role in message.author.roles]:
            return
        else:
            if message.channel.id == normalNA.id:
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                phrases = Configuration.getConfigVar(message.guild.id, "PHRASES")
                split = shlex.split(message.content.lower())
                if any(word in message.content.lower() for word in phrases):
                    response = await message.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{message.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await message.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(f"{message.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await message.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return
            #looking for normal EU
            if message.channel.id == normalEU.id: 
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                phrases = Configuration.getConfigVar(message.guild.id, "PHRASES")
                split = shlex.split(message.content.lower())
                if any(word in message.content.lower() for word in phrases):
                    response = await message.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{message.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await message.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(f"{message.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await message.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return
            #looking for ranked NA
            if message.channel.id == rankedNA.id:
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                phrases = Configuration.getConfigVar(message.guild.id, "PHRASES")
                split = shlex.split(message.content.lower())
                if any(word in message.content.lower() for word in phrases):
                    response = await message.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{message.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await message.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(f"{message.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await message.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return
            #looking for ranked EU
            if message.channel.id == rankedEU.id:
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                phrases = Configuration.getConfigVar(message.guild.id, "PHRASES")
                split = shlex.split(message.content.lower())
                if any(word in message.content.lower() for word in phrases):
                    response = await message.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{message.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await message.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(f"{message.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await message.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return
            #looking for normal Other
            if message.channel.id == normalOther.id:
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                phrases = Configuration.getConfigVar(message.guild.id, "PHRASES")
                split = shlex.split(message.content.lower())
                if any(word in message.content.lower() for word in phrases):
                    response = await message.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{message.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await message.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(f"{message.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await message.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return

            #looking for ranked Other
            if message.channel.id == rankedOther.id:
                unsupported = Configuration.getConfigVar(message.guild.id, "UNSUPPORTED")
                phrases = Configuration.getConfigVar(message.guild.id, "PHRASES")
                split = shlex.split(message.content.lower())
                if any(word in message.content.lower() for word in phrases):
                    response = await message.channel.send(f"{channelMessage}")
                    embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                    await logging.send(f"{message.author.id}")
                    await logging.send(embed=embed)
                for word in (w.lower() for w in unsupported):
                    if word in split:
                        response = await message.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"Filtered Word from Unsupported Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                        await logging.send(f"{message.author.id}")
                        await logging.send(embed=embed)
                        try:
                            await message.delete()
                        except NotFound as e:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                        else:
                            await asyncio.sleep(15)
                            await response.delete()
                            break
                else:
                    return
            #looking for Scrim NA
            if message.channel.id == scrimna.id:
                if message.author.id == 706269652724219987:
                    return
                if 679879783630372865 in [role.id for role in message.author.roles]:
                    return
                if 684144438251225099 in [role.id for role in message.author.roles]:
                    return
                else:
                    scrimNorthA = Configuration.getConfigVar(message.guild.id, "SCRIM-NA")
                    phrases = Configuration.getConfigVar(message.guild.id, "PHRASES")
                    split = shlex.split(message.content.lower())
                    if any(word in message.content.lower() for word in phrases):
                        response = await message.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                        await logging.send(f"{message.author.id}")
                        await logging.send(embed=embed)
                    for word in (w.lower() for w in scrimNorthA):
                        if word in split:
                            response = await message.channel.send(f"{channelMessage}")
                            embed = discord.Embed(title=f"Filtered Word from Scrim NA Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                            await logging.send(f"{message.author.id}")
                            await logging.send(embed=embed)
                            try:
                                await message.delete()
                            except NotFound as e:
                                await asyncio.sleep(15)
                                await response.delete()
                                break
                            else:
                                await asyncio.sleep(15)
                                await response.delete()
                                break
                    else:
                        return
            
            #looking for Scrim EU
            if message.channel.id == scrimeu.id:
                if message.author.id == 706269652724219987:
                    return
                if 679879783630372865 in [role.id for role in message.author.roles]:
                    return
                if 684144438251225099 in [role.id for role in message.author.roles]:
                    return
                else:
                    scrimEur = Configuration.getConfigVar(message.guild.id, "SCRIM-EU")
                    phrases = Configuration.getConfigVar(message.guild.id, "PHRASES")
                    split = shlex.split(message.content.lower())
                    if any(word in message.content.lower() for word in phrases):
                        response = await message.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                        await logging.send(f"{message.author.id}")
                        await logging.send(embed=embed)
                    for word in (w.lower() for w in scrimEur):
                        if word in split:
                            response = await message.channel.send(f"{channelMessage}")
                            embed = discord.Embed(title=f"Filtered Word from Scrim EU Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                            await logging.send(f"{message.author.id}")
                            await logging.send(embed=embed)
                            try:
                                await message.delete()
                            except NotFound as e:
                                await asyncio.sleep(15)
                                await response.delete()
                                break
                            else:
                                await asyncio.sleep(15)
                                await response.delete()
                                break
                    else:
                        return
            
            #looking for Scrim Other
            if message.channel.id == scrimother.id:
                if message.author.id == 706269652724219987:
                    return
                if 679879783630372865 in [role.id for role in message.author.roles]:
                    return
                if 684144438251225099 in [role.id for role in message.author.roles]:
                    return
                else:
                    scrimOth = Configuration.getConfigVar(message.guild.id, "SCRIM-OTHER")
                    phrases = Configuration.getConfigVar(message.guild.id, "PHRASES")
                    split = shlex.split(message.content.lower())
                    if any(word in message.content.lower() for word in phrases):
                        response = await message.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                        await logging.send(f"{message.author.id}")
                        await logging.send(embed=embed)
                    for word in (w.lower() for w in scrimOth):
                        if word in split:
                            response = await message.channel.send(f"{channelMessage}")
                            embed = discord.Embed(title=f"Filtered Word from Scrim Other Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                            await logging.send(f"{message.author.id}")
                            await logging.send(embed=embed)
                            try:
                                await message.delete()
                            except NotFound as e:
                                await asyncio.sleep(15)
                                await response.delete()
                                break
                            else:
                                await asyncio.sleep(15)
                                await response.delete()
                                break
                    else:
                        return

            #looking for Players
            if message.channel.id == lookingforplayers.id:
                if message.author.id == 706269652724219987:
                    return
                if 679879783630372865 in [role.id for role in message.author.roles]:
                    return
                if 684144438251225099 in [role.id for role in message.author.roles]:
                    return
                else:
                    lfplayers = Configuration.getConfigVar(message.guild.id, "LOOKINGFORPLAYERS")
                    phrases = Configuration.getConfigVar(message.guild.id, "PHRASES")
                    split = shlex.split(message.content.lower())
                    if any(word in message.content.lower() for word in phrases):
                        response = await message.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                        await logging.send(f"{message.author.id}")
                        await logging.send(embed=embed)
                    for word in (w.lower() for w in lfplayers):
                        if word in split:
                            response = await message.channel.send(f"{channelMessage}")
                            embed = discord.Embed(title=f"Filtered Word from Looking for Players Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                            await logging.send(f"{message.author.id}")
                            await logging.send(embed=embed)
                            try:
                                await message.delete()
                            except NotFound as e:
                                await asyncio.sleep(15)
                                await response.delete()
                                break
                            else:
                                await asyncio.sleep(15)
                                await response.delete()
                                break
                    else:
                        return
            
            #looking for Team
            if message.channel.id == lookingforteam.id:
                if message.author.id == 706269652724219987:
                    return
                if 679879783630372865 in [role.id for role in message.author.roles]:
                    return
                if 684144438251225099 in [role.id for role in message.author.roles]:
                    return
                else:
                    lfteam = Configuration.getConfigVar(message.guild.id, "LOOKINGFORTEAM")
                    phrases = Configuration.getConfigVar(message.guild.id, "PHRASES")
                    split = shlex.split(message.content.lower())
                    if any(word in message.content.lower() for word in phrases):
                        response = await message.channel.send(f"{channelMessage}")
                        embed = discord.Embed(title=f"{loggingtitle}", description=f"{loggingmessage}It contained the following phrase: **{phrases}**", color=0xff7171)
                        await logging.send(f"{message.author.id}")
                        await logging.send(embed=embed)
                    for word in (w.lower() for w in lfteam):
                        if word in split:
                            response = await message.channel.send(f"{channelMessage}")
                            embed = discord.Embed(title=f"Filtered Word from Looking for Team Category", description=f"Found message from {message.author.name}#{message.author.discriminator} ({message.author.mention}) (``{message.author.id}``) in {message.channel.mention} containing blacklisted word **{word}**:\n\n```{message.content}```", color=0xff7171)
                            await logging.send(f"{message.author.id}")
                            await logging.send(embed=embed)
                            try:
                                await message.delete()
                            except NotFound as e:
                                await asyncio.sleep(15)
                                await response.delete()
                                break
                            else:
                                await asyncio.sleep(15)
                                await response.delete()
                                break
                    else:
                        return
            else:
                return
                 
def setup(bot):
    bot.add_cog(lookingfor(bot))
