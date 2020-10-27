import asyncio
import datetime
import discord
import configparser
import os
import time
import traceback
import logging

from discord.ext import commands
from discord.ext.commands import BucketType, BadArgument, MissingPermissions
from discord import abc, TextChannel, Role
from discord.abc import PrivateChannel
from utils import Util, Configuration
from argparse import ArgumentParser

class admin(commands.Cog):
    def __init__(self, bot):
        pass


    @commands.command()
    async def restart(self, ctx:commands.Context):
        """Restarts the bot."""
        if ctx.author.id == 298618155281154058:
            await ctx.send("Restarting!")
            await self.bot.close()
        else:
            return
            
    @commands.guild_only()
    @commands.group(hidden=True)
    @commands.has_permissions(manage_roles=True)
    async def configure(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
                embed=discord.Embed(title="Configuration", description="**There are several ways to configure the bot, you can follow the instructions as described here:**", color=0xff9494, timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                await ctx.send(embed=embed)
        else:
            return

    @commands.guild_only()
    @configure.command()
    async def emergencyrole(self, ctx: commands.Context, *, role: discord.Role):
        if role is None:
            embed=discord.Embed(title="Error on Setting Emergency Role", description=":warning: I was not able to add the roleID that you specified, please make sure that the role that you are trying to specify exists.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            try:
                Configuration.setConfigVar(ctx.guild.id, "EMERGENCY", role.id)
                embed = discord.Embed(colour=discord.Colour(0x77dd77),title='Emergency Role Successfully Set!', description=f"{role.mention} has been successfully added as Emergency role",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            except (BadArgument) as ex:
                embed=discord.Embed(title="Invalid Role on Setting Emergency Role", description=f":warning: It would appear that this command: ``{ctx.message.context}\n\n{ex}`` did not contain a valid roleID, please make sure to provide me with the correct roleID and try again.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

    @commands.guild_only()
    @configure.command()
    async def fakeemergencyrole(self, ctx: commands.Context, *, role: discord.Role):
        if role is None:
            embed=discord.Embed(title="Error on Setting Fake Emergency Role", description=":warning: I was not able to add the roleID that you specified, please make sure that the role that you are trying to specify exists.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            try:
                Configuration.setConfigVar(ctx.guild.id, "FAKEEMERGENCY", role.id)
                embed = discord.Embed(colour=discord.Colour(0x77dd77),title='Fake Emergency Role Successfully Set!', description=f"{role.mention} has been successfully added as Emergency role",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            except (BadArgument) as ex:
                embed=discord.Embed(title="Invalid Role on Setting Fake Emergency Role", description=f":warning: It would appear that this command: ``{ctx.message.context}\n\n{ex}`` did not contain a valid roleID, please make sure to provide me with the correct roleID and try again.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
    
    @commands.guild_only()
    @configure.command()
    async def pullroomrole(self, ctx: commands.Context, *, role: discord.Role):
        if role is None:
            embed=discord.Embed(title="Error on Setting Pullroom Role", description=":warning: I was not able to add the roleID that you specified, please make sure that the role that you are trying to specify exists.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            try:
                Configuration.setConfigVar(ctx.guild.id, "PULLROOMROLE", role.id)
                embed = discord.Embed(colour=discord.Colour(0x77dd77),title='Pullroom Role Successfully Set!', description=f"{role.mention} has been successfully added as Pullroom role",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            except (BadArgument) as ex:
                embed=discord.Embed(title="Invalid Role on Setting Pullroom Role", description=f":warning: It would appear that this command: ``{ctx.message.context}\n\n{ex}`` did not contain a valid roleID, please make sure to provide me with the correct roleID and try again.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
    
    @commands.guild_only()
    @configure.command()
    async def pullroom(self, ctx: commands.Context, *, channel:discord.TextChannel):
        if channel is None:
            embed=discord.Embed(title="Error on Setting Pullroom Channel", description=":warning: I was not able to add the channelID that you specified, please make sure that the channel that you are trying to specify exists.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            try:
                Configuration.setConfigVar(ctx.guild.id, "PULLROOM", channel.id)
                embed = discord.Embed(colour=discord.Colour(0x77dd77),title='Pullroom Channel Successfully Set!', description=f"{channel.mention} has been successfully added as Pullroom.",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            except (BadArgument) as ex:
                embed=discord.Embed(title="Invalid Channel on Setting Pullroom Channel", description=f":warning: It would appear that this command: ``{ctx.message.context}\n\n{ex}`` did not contain a valid channelID, please make sure to provide me with the correct channelID and try again.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
    
    @commands.guild_only()
    @configure.command()
    async def pullroomlog(self, ctx: commands.Context, *, channel:discord.TextChannel):
        if channel is None:
            embed=discord.Embed(title="Error on Setting Pullroom Log Channel", description=":warning: I was not able to add the channelID that you specified, please make sure that the channel that you are trying to specify exists.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            try:
                Configuration.setConfigVar(ctx.guild.id, "PULLROOMLOG", channel.id)
                embed = discord.Embed(colour=discord.Colour(0x77dd77),title='Pullroom Log Channel Successfully Set!', description=f"{channel.mention} has been successfully added as Pullroom Logging.",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            except (BadArgument) as ex:
                embed=discord.Embed(title="Invalid Channel on Setting Pullroom Log Channel", description=f":warning: It would appear that this command: ``{ctx.message.context}\n\n{ex}`` did not contain a valid channelID, please make sure to provide me with the correct channelID and try again.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
    
    @commands.guild_only()
    @configure.command()
    async def modrole(self, ctx: commands.Context, *, role: discord.Role):
        if role is None:
            embed=discord.Embed(title="Error on Setting Mod Role", description=":warning: I was not able to add the roleID that you specified, please make sure that the role that you are trying to specify exists.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            try:
                Configuration.setConfigVar(ctx.guild.id, "MODROLE", role.id)
                embed = discord.Embed(colour=discord.Colour(0x77dd77),title='Mod Role Successfully Set!', description=f"{role.mention} has been successfully added as mod role.",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            except (BadArgument) as ex:
                embed=discord.Embed(title="Invalid Role on Setting Mod Role", description=f":warning: It would appear that this command: ``{ctx.message.context}\n\n{ex}`` did not contain a valid roleID, please make sure to provide me with the correct roleID and try again.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

    @commands.guild_only()
    @configure.command()
    async def normalna(self, ctx: commands.Context, *, channel:discord.TextChannel):
        if channel is None:
            embed=discord.Embed(title="Error on Setting Non-Ranked NA Channel", description=":warning: I was not able to add the channelID that you specified, please make sure that the channel that you are trying to specify exists.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            try:
                Configuration.setConfigVar(ctx.guild.id, "NONRANKED-NA", channel.id)
                embed = discord.Embed(colour=discord.Colour(0x77dd77),title='Non-Ranked NA channel Successfully Set!', description=f"{channel.mention} has been successfully added as non-ranked NA.",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            except (BadArgument) as ex:
                embed=discord.Embed(title="Invalid Channel on Setting NonRanked NA Channel", description=f":warning: It would appear that this command: ``{ctx.message.context}\n\n{ex}`` did not contain a valid channelID, please make sure to provide me with the correct channelID and try again.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)     

    @commands.guild_only()
    @configure.command()
    async def normaleu(self, ctx: commands.Context, *, channel:discord.TextChannel):
        if channel is None:
            embed=discord.Embed(title="Error on Setting Non-Ranked EU Channel", description=":warning: I was not able to add the channelID that you specified, please make sure that the channel that you are trying to specify exists.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            try:
                Configuration.setConfigVar(ctx.guild.id, "NONRANKED-EU", channel.id)
                embed = discord.Embed(colour=discord.Colour(0x77dd77),title='Non-Ranked EU Channel Successfully Set!', description=f"{channel.mention} has been successfully added as non-ranked EU.",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            except (BadArgument) as ex:
                embed=discord.Embed(title="Invalid Channel on Setting NonRanked EU Channel", description=f":warning: It would appear that this command: ``{ctx.message.context}\n\n{ex}`` did not contain a valid channelID, please make sure to provide me with the correct channelID and try again.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)       
                
    @commands.guild_only()
    @configure.command()
    async def normalother(self, ctx: commands.Context, *, channel:discord.TextChannel):
        if channel is None:
            embed=discord.Embed(title="Error on Setting Non-Ranked Other Channel", description=":warning: I was not able to add the channelID that you specified, please make sure that the channel that you are trying to specify exists.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            try:
                Configuration.setConfigVar(ctx.guild.id, "NONRANKED-OTHER", channel.id)
                embed = discord.Embed(colour=discord.Colour(0x77dd77),title='Non-Ranked Other Channel Successfully Set!', description=f"{channel.mention} has been successfully added as non-ranked Other.",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            except (BadArgument) as ex:
                embed=discord.Embed(title="Invalid Channel on Setting NonRanked Other Channel", description=f":warning: It would appear that this command: ``{ctx.message.context}\n\n{ex}`` did not contain a valid channelID, please make sure to provide me with the correct channelID and try again.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)     

    @commands.guild_only()
    @configure.command()
    async def rankedna(self, ctx: commands.Context, *, channel:discord.TextChannel):
        if channel is None:
            embed=discord.Embed(title="Error on Setting Ranked NA Channel", description=":warning: I was not able to add the channelID that you specified, please make sure that the channel that you are trying to specify exists.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            try:
                Configuration.setConfigVar(ctx.guild.id, "RANKED-NA", channel.id)
                embed = discord.Embed(colour=discord.Colour(0x77dd77),title='Ranked NA Channel Successfully Set!', description=f"{channel.mention} has been successfully added as ranked NA.",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            except (BadArgument) as ex:
                embed=discord.Embed(title="Invalid Channel on Setting Ranked NA Channel", description=f":warning: It would appear that this command: ``{ctx.message.context}\n\n{ex}`` did not contain a valid channelID, please make sure to provide me with the correct channelID and try again.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)  
    
    @commands.guild_only()
    @configure.command()
    async def rankedeu(self, ctx: commands.Context, *, channel:discord.TextChannel):
        if channel is None:
            embed=discord.Embed(title="Error on Setting Ranked EU Channel", description=":warning: I was not able to add the channelID that you specified, please make sure that the channel that you are trying to specify exists.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            try:
                Configuration.setConfigVar(ctx.guild.id, "RANKED-EU", channel.id)
                embed = discord.Embed(colour=discord.Colour(0x77dd77),title='Ranked EU Channel Successfully Set!', description=f"{channel.mention} has been successfully added as ranked EU.",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            except (BadArgument) as ex:
                embed=discord.Embed(title="Invalid Channel on Setting Ranked EU Channel", description=f":warning: It would appear that this command: ``{ctx.message.context}\n\n{ex}`` did not contain a valid channelID, please make sure to provide me with the correct channelID and try again.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)  

    @commands.guild_only()
    @configure.command()
    async def rankedother(self, ctx: commands.Context, *, channel:discord.TextChannel):
        if channel is None:
            embed=discord.Embed(title="Error on Setting Ranked Other Channel", description=":warning: I was not able to add the channelID that you specified, please make sure that the channel that you are trying to specify exists.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            try:
                Configuration.setConfigVar(ctx.guild.id, "RANKED-OTHER", channel.id)
                embed = discord.Embed(colour=discord.Colour(0x77dd77),title='Ranked Other Channel Successfully Set!', description=f"{channel.mention} has been successfully added as ranked Other.",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            except (BadArgument) as ex:
                embed=discord.Embed(title="Invalid Channel on Setting Ranked Other Channel", description=f":warning: It would appear that this command: ``{ctx.message.context}\n\n{ex}`` did not contain a valid channelID, please make sure to provide me with the correct channelID and try again.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)  
    
    @commands.guild_only()
    @configure.command()
    async def logging(self, ctx: commands.Context, *, channel:discord.TextChannel):
        if channel is None:
            embed=discord.Embed(title="Error on Setting Logging Channel", description=":warning: I was not able to add the channelID that you specified, please make sure that the channel that you are trying to specify exists.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            try:
                Configuration.setConfigVar(ctx.guild.id, "LOGGING", channel.id)
                embed = discord.Embed(colour=discord.Colour(0x77dd77),title='Logging Channel Successfully Set!', description=f"{channel.mention} has been successfully added as logging channel. I will now log anything that I catch from LFG rooms.",timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            except (BadArgument) as ex:
                embed=discord.Embed(title="Invalid Channel on Setting Logging Channel", description=f":warning: It would appear that this command: ``{ctx.message.context}\n\n{ex}`` did not contain a valid channelID, please make sure to provide me with the correct channelID and try again.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)  

    @commands.guild_only()
    @commands.command()
    async def notemergency(self, ctx: commands.Context, *, word: str):
        modrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "MODROLE"))
        if modrole not in ctx.author.roles:
            return
        else:
            blacklist = Configuration.getConfigVar(ctx.guild.id, "NONEMERGENCY")
            if word in blacklist:
                blacklist.remove(word)
                await ctx.send(f"I have removed ``{word}`` from the list I will no longer keep an eye out in any future Emergency role usage!")
                Configuration.setConfigVar(ctx.guild.id, "NONEMERGENCY", blacklist)
            else: 
                blacklist.append(word)
                await ctx.send(f"I have added ``{word}`` to the list for me to keep a eye out in any future Emergency role usage!")
                Configuration.setConfigVar(ctx.guild.id, "NONEMERGENCY", blacklist)


def setup(bot):
    bot.add_cog(admin(bot))
