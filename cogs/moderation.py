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
from discord import abc, Forbidden, NotFound
from discord.abc import PrivateChannel
from utils import Util, Configuration
from argparse import ArgumentParser

class moderation(commands.Cog):
    def __init__(self, bot):
        pass
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id == 679875946597056683:
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
                censor = Configuration.getConfigVar(message.guild.id, "CENSOR")
                if any(word in message.content.lower() for word in censor):
                    response = await message.channel.send(f"Please do not send messages containing any of the censored words / invites.")
                    logging = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "PULLROOMLOG"))
                    embed = discord.Embed(title=f"Filtered Message in Censor", description=f"Found message from {message.author.name}#{message.author.discriminator} (``{message.author.id}``) in {message.channel.mention} containing:\n\n```{message.content}```", color=0xff7171)
                    await logging.send(embed=embed)
                    asyncio.sleep(15)
                    await message.delete()
                    await response.delete()
        else:
            return  

    #This allows the moderator to pull the user into a private channel to discuss with them.
    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    async def pull(self, ctx: commands.Context, member: discord.User, *, reason=""):
        channel = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "PULLROOM"))
        pullroomrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "PULLROOMROLE"))
        logs = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "PULLROOMLOG"))
        modrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "MODROLE"))
        user = ctx.guild.get_member(member.id)
        if modrole not in ctx.author.roles:
            return
        else:
            if ctx.guild.get_member(member.id) is None:
                embed=discord.Embed(title="Unknown Member Error", description=f":warning: I was not able to add {member.name}#{member.discriminator} (``{member.id}``) to the pullroom. It seems like they likely left this server or was kicked by a moderator.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
            if reason is None:
                reason = "No reason provided."
            if channel is None:
                embed=discord.Embed(title="Unknown Channel Error", description=f":warning: I was not able to add {member.name}#{member.discriminator} (``{member.id}``) to the pullroom. It seems like that the channel is not configured, please have a Senior Moderator or a Bot Developer to fix this. \n\nIf this persists, contact Ghoul.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            if pullroomrole is None:
                embed=discord.Embed(title="Unknown Role Error", description=f":warning: I was not able to add {member.name}#{member.discriminator} (``{member.id}``) to the pullroom. It seems like that the role required is not configured, please have a Senior Moderator or a Bot Developer to fix this. \n\nIf this persists, contact Ghoul.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                if pullroomrole not in user.roles:
                    try:
                        await user.add_roles(pullroomrole)
                    except discord.Forbidden as e:
                        embed=discord.Embed(title="Cannot add Pullroom role", description=f":warning: I was not able to add {member.name}#{member.discriminator} (``{member.id}``) to the pullroom. It would appear that I do not have Manage Roles permission to continue, please have a Senior Moderator or a Bot Developer to fix this. \n\nIf this persists, contact Ghoul.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                        embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                        await ctx.send(embed=embed)
                    else:
                        try:
                            await channel.send(f"{member.mention}, you are requested to speak with a moderator one to one.")
                            embed=discord.Embed(title="Pullroom Request", description=f"**User:** {member.mention} - {member.name}#{member.discriminator} (``{member.id}``)\n\n**Reason**: {reason}", color=0xff9494, timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                            embed.set_thumbnail(url=member.avatar_url)
                            embed.set_footer(text="Remember, the user cannot see this conversation until they open this channel.")
                            await channel.send(embed=embed)
                            await ctx.send(f"Successfully pulled the user into {channel.mention}")
                            embed2=discord.Embed(title="Pullroom Add Log", description=f"{ctx.author.mention} (``{ctx.author.id}``) pulled {member.name}#{member.discriminator} (``{member.id}``) into the pullroom.\n\n**Reason:** {reason}", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                            embed2.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                            embed2.set_thumbnail(url=member.avatar_url)
                            await logs.send(embed=embed2)
                        except discord.Forbidden as e:
                            embed=discord.Embed(title="Cannot send message to the pullroom", description=f":warning: I was not able to send a message in the pullroom. It would appear that I do not have permission to continue, please have a Senior Moderator or a Bot Developer to fix this. \n\nIf this persists, contact Ghoul.\n\n**Error:**\n{e}", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                            await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title="User in Pullroom", description=f":warning: {member.mention} - {member.name}#{member.discriminator} (``{member.id}``) is already in the pullroom! Either you added them already and forgot about them or someone else is handling the user.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                    embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                    embed.set_thumbnail(url=member.avatar_url)
                    await ctx.send(embed=embed)
        
    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    async def remove(self, ctx: commands.Context, member: discord.User, *, reason=""):
        channel = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "PULLROOM"))
        pullroomrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "PULLROOMROLE"))
        logs = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "PULLROOMLOG"))
        modrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "MODROLE"))
        user = ctx.guild.get_member(member.id)
        if modrole not in ctx.author.roles:
            return
        if ctx.guild.get_member(member.id) is None:
            embed=discord.Embed(title="Unknown Member Error", description=f":warning: I was not able to remove {member.name}#{member.discriminator} (``{member.id}``) from the pullroom. It seems like they likely left this server or was kicked by a moderator.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=embed)
        else:
            if reason is None:
                reason = "No reason provided."
            if channel is None:
                embed=discord.Embed(title="Unknown Channel Error", description=f":warning: I was not able to remove {member.name}#{member.discriminator} (``{member.id}``) from the pullroom. It seems like that the channel is not configured, please have a Senior Moderator or a Bot Developer to fix this. \n\nIf this persists, contact Ghoul.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            if pullroomrole is None:
                embed=discord.Embed(title="Unknown Role Error", description=f":warning: I was not able to remove {member.name}#{member.discriminator} (``{member.id}``) from the pullroom. It seems like that the role required is not configured, please have a Senior Moderator or a Bot Developer to fix this. \n\nIf this persists, contact Ghoul.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                if pullroomrole in user.roles:
                    try:
                        await user.remove_roles(pullroomrole)
                    except discord.Forbidden as e:
                        embed=discord.Embed(title="Cannot remove Pullroom role", description=f":warning: I was not able to remove {member.name}#{member.discriminator} (``{member.id}``) from the pullroom. It would appear that I do not have Manage Roles permission to continue, please have a Senior Moderator or a Bot Developer to fix this. \n\nIf this persists, contact Ghoul.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                        embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                        await ctx.send(embed=embed)
                    else:
                        try:
                            embed=discord.Embed(title="Removed User from Pullroom", description=f"**User:** {member.mention} - {member.name}#{member.discriminator} (``{member.id}``)\n\n**Conclusion**: {reason}", color=0xff9494, timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                            embed.set_thumbnail(url=member.avatar_url)
                            await channel.send(embed=embed)
                            await ctx.send(f"Successfully pulled the user from {channel.mention}")
                            embed2=discord.Embed(title="Pullroom Removal Log", description=f"{ctx.author.mention} (``{ctx.author.id}``) pulled {member.name}#{member.discriminator} (``{member.id}``) from the pullroom.\n\n**Conclusion:** {reason}", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                            embed2.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                            embed2.set_thumbnail(url=member.avatar_url)
                            await logs.send(embed=embed2)
                        except discord.Forbidden as e:
                            embed=discord.Embed(title="Cannot send message to the pullroom", description=f":warning: I was not able to send a message in the pullroom. It would appear that I do not have permission to continue, please have a Senior Moderator or a Bot Developer to fix this. \n\nIf this persists, contact Ghoul.\n\n**Error:**\n{e}", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                            await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title="User no longer in Pullroom", description=f":warning: {member.mention} - {member.name}#{member.discriminator} (``{member.id}``) seems to be no longer in the pullroom. Either that someone else used the command or manually removed the role.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                    embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                    embed.set_thumbnail(url=member.avatar_url)
                    await ctx.send(embed=embed)        




def setup(bot):
    bot.add_cog(moderation(bot))
