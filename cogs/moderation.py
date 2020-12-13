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
from discord.ext.commands import BucketType, BadArgument
from discord import abc, Forbidden, NotFound
from discord.abc import PrivateChannel
from discord import utils
from utils import Util, Configuration
from utils.Util import confirm_command, confirm_command2
from argparse import ArgumentParser

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_timeStamp = datetime.datetime.utcfromtimestamp(0)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        censor = Configuration.getConfigVar(message.guild.id, "NONEMERGENCY")
        emergencyrole = message.guild.get_role(Configuration.getConfigVar(message.guild.id, "EMERGENCY"))
        fake = message.guild.get_role(Configuration.getConfigVar(message.guild.id, "FAKEEMERGENCY"))
        logging = message.guild.get_channel(Configuration.getConfigVar(message.guild.id, "LOGGING"))
        time_difference = (datetime.datetime.utcnow() - self.last_timeStamp).total_seconds()
        if fake is None:
            return
        if message.guild.id == 679875946597056683:
            if 684144438251225099 in [role.id for role in message.author.roles]:
                return
            if message.author.id == 706269652724219987:
                return
            else:
                if fake.mention == message.content:
                    embed6=discord.Embed(title="Invalid Emergency Reason!", description=f"Hmmmm... Seems like you did not provide any reason for me to ping the emergency role. Here are the list of valid reasons to ping Emergency role, if you still believe that this is something that would require the moderators' attention then please contact our modmail at <@711678018573303809>!\n\n- Raid\n- NSFW content (porngraphy or gore)", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                    response = await message.channel.send(embed=embed6)
                    embed8=discord.Embed(title="Invalid Emergency Usage Detected", description=f"{message.author.name}#{message.author.discriminator} ({message.author.mention}) - (``{message.author.id}``) **attempted** to use the Emergency role in {message.channel.mention}, but they did not provide any reason at all! Either this may be some kind of test, or they are attempting to abuse it.", color=0xff7171)
                    await logging.send(f"{message.author.id}")
                    await logging.send(embed=embed8)
                    await asyncio.sleep(15)
                    await message.delete()
                    await response.delete()
                    return
                if fake.mention in message.content:
                    if time_difference < 600:
                        cool = await message.channel.send("It looks like that someone has used the emergency ping recently. Please wait for a bit before trying again, if it's urgent then please contact the mods at <@711678018573303809>")
                        embed9=discord.Embed(title= "Emergency Usage on Cooldown!", description=f"{message.author.name}#{message.author.discriminator} ({message.author.mention}) - (``{message.author.id}``) **attempted** to use the Emergency role in {message.channel.mention}, but the Emergency role was pinged too recently. They've been informed to use our Modmail is there is an actual emergency. Here is the context: ```{message.content}```", color=0xff7171)
                        await logging.send(f"{message.author.id}")
                        await logging.send(embed=embed9)
                        await asyncio.sleep(15)
                        await message.delete()
                        await cool.delete()
                    else:
                        if any(word in message.content.lower() for word in censor):
                            embed6=discord.Embed(title="Invalid Emergency Reason!", description=f"Hmmmm... Seems like you did not provide the valid reason for me to ping the emergency role. Here are the list of valid reasons to ping Emergency role, if you still believe that this is something that would require the moderators' attention then please contact our modmail at <@711678018573303809>!\n\n- Raid\n- NSFW content (porngraphy or gore)", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                            response = await message.channel.send(embed=embed6)
                            embed10=discord.Embed(title= "Possible Emergency Abuse!", description=f"{message.author.name}#{message.author.discriminator} ({message.author.mention}) - (``{message.author.id}``) **attempted** to use the Emergency role in {message.channel.mention}, but the Emergency reason did not seem like it was urgent. They've been informed to use our Modmail is there is an actual emergency. Here is the context: ```{message.content}```", color=0xff7171)
                            await logging.send(f"{message.author.id}")
                            await logging.send(embed=embed10)
                            await asyncio.sleep(15)
                            await message.delete()
                            await response.delete()
                            return
                        else:
                            async def yes():
                                if emergencyrole is None:
                                    embed3=discord.Embed(title="Unconfigured Emergency role!", description=f"Hmmmm... Seems like the emergency role is not configured. Please contact the mods over at the Modmail at <@711678018573303809>", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                                    riprole = await message.channel.send(embed=embed3)
                                    await asyncio.sleep(15)
                                    await riprole.delete()
                                    await message.delete()
                                    return
                                else:
                                    await message.channel.send(f"{emergencyrole.mention}, someone needs your assistance. Please ensure that this matter is solved appropriately.")
                                    embed4=discord.Embed(title="Emergency Situation!", description=f"{message.author.mention} ({message.author.name}#{message.author.discriminator} (``{message.author.id}``) has pinged the Emergency role with ``{message.content}``.", color=0xff9494, timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                                    await message.channel.send(embed=embed4)
                                    embed11=discord.Embed(title= "Emergency Usage Detected!", description=f"{message.author.name}#{message.author.discriminator} ({message.author.mention}) - (``{message.author.id}``) **attempted** to use the Emergency role in {message.channel.mention}, but the attempt was successful as I did not find anything in my list to mark it invalid! Here is the context for anyone wanting to know the ping: ```{message.content}```", color=0x77dd77)
                                    await logging.send(f"{message.author.id}")
                                    await logging.send(embed=embed11)
                                    self.last_timeStamp = datetime.datetime.utcnow()
                            embed = discord.Embed(title="You are about to ping the Emergency role", description="By pinging the Emergency role, you are about to summon our moderation team. **Are you sure that you are using the Emergency ping for the following reasons:**\n\n- Raid\n\n- Major spam\n\n- NSFW content", color=0xff7171)
                            msg = await message.channel.send(embed=embed)
                            await confirm_command2(self, message, msg, on_yes=yes)
                else:
                    return
        else:
            return

    @commands.command()
    @commands.guild_only() 
    @commands.cooldown(1, 600, BucketType.guild)   
    @commands.bot_has_permissions(add_reactions=True)
    async def emergency(self, ctx: commands.Context, *, reason=""):
        """Uses the emergency ping!"""
        bademergency = Configuration.getConfigVar(ctx.guild.id, "NONEMERGENCY")
        emergencyrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "EMERGENCY"))
        logging = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "LOGGING"))
        if reason == "":
            embed=discord.Embed(title="Invalid Emergency Reason!", description=f"It looks like that you did not provide a reason required for me to ping the Emergency ping. Please provide the correct reason before trying again!", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            await ctx.send(embed=embed)
            embed8=discord.Embed(title="Invalid Emergency Usage Detected", description=f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.mention}) - (``{ctx.author.id}``) **attempted** to use the Emergency role in {ctx.channel.mention}, but they did not provide any reason at all! Either this may be some kind of test, or they are attempting to abuse it.", color=0xff7171)
            await logging.send(f"{ctx.author.id}")
            await logging.send(embed=embed8) 
            ctx.command.reset_cooldown(ctx)
            return
        
        if any(word in reason.lower() for word in bademergency):
            embed6=discord.Embed(title="Invalid Emergency Reason!", description=f"Hmmmm... Seems like you did not provide the valid reason for me to ping the emergency role. Here are the list of valid reasons to ping Emergency role, if you still believe that this is something that would require the moderators' attention then please contact our modmail at <@711678018573303809>!\n\n- Raid\n- NSFW content (porngraphy or gore)", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            baduser = await ctx.send(embed=embed6)
            embed10=discord.Embed(title= "Possible Emergency Abuse!", description=f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.mention}) - (``{ctx.author.id}``) **attempted** to use the Emergency role in {ctx.channel.mention}, but the Emergency reason did not seem like it was urgent. They've been informed to use our Modmail is there is an actual emergency. Here is the context: ```>emergency {reason}```", color=0xff7171)
            await logging.send(f"{ctx.author.id}")
            await logging.send(embed=embed10)
            await asyncio.sleep(15)
            await baduser.delete()
            await ctx.message.delete()
            ctx.command.reset_cooldown(ctx)
            return

        async def yes():
            if emergencyrole is None:
                embed3=discord.Embed(title="Unconfigured Emergency role!", description=f"Hmmmm... Seems like the emergency role is not configured. Please contact the mods over at the Modmail at <@711678018573303809>", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                riprole = await ctx.send(embed=embed3)
                await asyncio.sleep(15)
                await riprole.delete()
                await ctx.message.delete()
                ctx.command.reset_cooldown(ctx)
                return

            else:
                await ctx.send(f"{emergencyrole.mention}, someone needs your assistance. Please ensure that this matter is solved appropriately.")
                embed4=discord.Embed(title="Emergency Situation!", description=f"{ctx.author.mention} ({ctx.author.name}#{ctx.author.discriminator} (``{ctx.author.id}``) has pinged the Emergency role for ``{reason}``.", color=0xff9494, timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                await ctx.send(embed=embed4)
                embed11=discord.Embed(title= "Emergency Usage Detected!", description=f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.mention}) - (``{ctx.author.id}``) **attempted** to use the Emergency role in {ctx.channel.mention}, but the attempt was successful as I did not find anything in my list to mark it invalid! Here is the context for anyone wanting to know the ping: ```>emergency {reason}```", color=0x77dd77)
                await logging.send(f"{ctx.author.id}")
                await logging.send(embed=embed11)
                
        embed2=discord.Embed(title="Emergency Ping Warning", description=f"Are you ABSOLUTELY sure that you want to ping the Emergency role for this reason: ``{reason}``?\n\nMake sure that the reason that you are pinging the emergency role meets the following (if it does not meet the following requirements but you feel like you need the moderators' attention, please contact us at <@711678018573303809>.) :\n\n- Major raid\n- NSFW content in channel", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
        msg = await ctx.send(embed=embed2)
        await confirm_command(ctx, msg, on_yes=yes)
    

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx:commands.Context):
        """Pings to see if the bot is alive."""
        modrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "MODROLE"))
        if modrole not in ctx.author.roles:
            return
        else:
            await ctx.send("Ping, pong! I am still alive! :heart:")

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
        if reason == "":
            return await ctx.send("Please make sure to provide a reason why you're pulling the user in!")
        if modrole not in ctx.author.roles:
            return
        if ctx.author.id == member.id:
            await ctx.send("Sorry, I am unable to help you to pull yourself in the pullroom.")
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
                    except discord.NotFound as e:
                        embed=discord.Embed(title="Unknown Member Error", description=f":warning: I was not able to add {member} to the pullroom. Please verify to ensure that the userID that you provided is correct.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                        embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                        return await ctx.send(embed=embed)
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
    @pull.error
    async def pull_error(ctx, error):
        if isinstance(error, commands.NotFound):
            embed=discord.Embed(title="Unknown Member Error", description=f":warning: I was not able to add {member} to the pullroom. Please verify to ensure that the userID that you provided is correct.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed=discord.Embed(title="Unknown Member Error", description=f":warning: I was not able to add {member} to the pullroom. Please verify to ensure that the userID that you provided is correct.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=embed)
        
    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    async def remove(self, ctx: commands.Context, member: discord.User, *, reason=""):
        channel = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "PULLROOM"))
        pullroomrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "PULLROOMROLE"))
        logs = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "PULLROOMLOG"))
        modrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "MODROLE"))
        user = ctx.guild.get_member(member.id)
        if reason == "":
            return await ctx.send("Please make sure to provide a reason why you're removing the user from the pullroom!")
        if modrole not in ctx.author.roles:
            return
        if ctx.author.id == member.id:
            await ctx.send("Sorry, I am unable to help you to pull yourself in the pullroom.")
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
                    except discord.NotFound as e:
                        embed=discord.Embed(title="Unknown Member Error", description=f":warning: I was not able to add {member} to the pullroom. Please verify to ensure that the userID that you provided is correct.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                        embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                        return await ctx.send(embed=embed)
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
    @remove.error
    async def remove_error(ctx, error):
        if isinstance(error, commands.NotFound):
            embed=discord.Embed(title="Unknown Member Error", description=f":warning: I was not able to remove {member} from the pullroom. Please verify to ensure that the userID that you provided is correct.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed=discord.Embed(title="Unknown Member Error", description=f":warning: I was not able to remove {member} from the pullroom. Please verify to ensure that the userID that you provided is correct.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            




def setup(bot):
    bot.add_cog(moderation(bot))
