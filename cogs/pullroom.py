import discord
import datetime
import time
import asyncio
from utils import Configuration

from discord.ext import commands

class pullroom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        print(f"Message from {message.author.name} in {message.guild.id} returned.")
        self.bot.process_commands(message)

    @commands.command()
    @commands.guild_only()
    async def testcommand(self, ctx: commands.Context):
        print ("hello")
        await ctx.send("Test is done.")
    ### The two command related stuff is for debugging purposes only. 
    
    @commands.command()
    @commands.guild_only()
    async def pull(self, ctx: commands.Context, member: discord.User, *, reason=""):
        channel = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "PULLROOM"))
        logging = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "PULLROOMLOG"))
        pullroomrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "PULLROOMROLE"))
        modrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "MODROLE"))
        adminrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "ADMINROLE"))
        roles = [modrole.id, adminrole.id]
        user_roles = [role.id for role in ctx.author.roles]
        verify = await self.bot.fetch_user(member.id)
        user = ctx.guild.get_member(verify.id)
        if len(set(roles) & set(user_roles)) == 0:
            return
        if ctx.author.id == member.id:
            await ctx.send("Sorry, I am unable to help you to pull yourself in the pullroom.")
        if reason == "":
            await ctx.send("Please specify a reason that you are pulling the user in!")
            return
        if pullroomrole is None:
                embed=discord.Embed(title="Unknown Role Error", description=f":warning: I was not able to add {member.name}#{member.discriminator} (``{member.id}``) to the pullroom. It seems like that the role required is not configured, please have a Senior Moderator or a Bot Developer to fix this. \n\nIf this persists, contact Ghoul.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.display_avatar)
                await ctx.send(embed=embed)
                return
        if pullroomrole in user.roles:
            await ctx.send("This user already got the pullroom role, likely from the old systems. Remove the role and try again.")
            return
        else:
            if pullroomrole not in user.roles:
                try:
                    await user.add_roles(pullroomrole)
                except discord.Forbidden as e:
                    embed=discord.Embed(title="Cannot add Pullroom role", description=f":warning: I was not able to add {member.name}#{member.discriminator} (``{member.id}``) to the pullroom. It would appear that I do not have Manage Roles permission to continue, please have a Senior Moderator or a Bot Developer to fix this. \n\nIf this persists, contact Ghoul.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                    embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.display_avatar)
                    await ctx.send(embed=embed)
                except discord.NotFound as e:
                    embed=discord.Embed(title="Unknown Member Error", description=f":warning: I was not able to add {member} to the pullroom. Please verify to ensure that the userID that you provided is correct.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                    embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.display_avatar)
                    return await ctx.send(embed=embed)
                else:
                    await ctx.send(f"Creating a pullroom thread for ``{user.name}#{user.discriminator}`` (``{user.id}``)")
                    pullthread = await channel.create_thread(name=f"{user.name}-{user.discriminator} Pullroom", message=None, auto_archive_duration=60, type=None, reason = f"Pullroom request for {user.name}#{user.discriminator} ({user.id}) made by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", invitable = False, slowmode_delay = None)
                    embed=discord.Embed(title="Pullroom Request", description=f"**User:** {user.mention} - {user.name}#{user.discriminator} (``{user.id}``)\n\n**Reason**: {reason}", color=0xff9494)
                    embed.set_thumbnail(url=member.display_avatar)
                    embed.set_footer(text="Remember to still follow rules when speaking in pullroom with a moderator, further moderation actions will be taken if there are rule violations.")
                    await pullthread.send(f"{ctx.author.mention} would like to speak with you in this pullroom thread, {user.mention}.")
                    await pullthread.send(embed=embed)
                    embed3=discord.Embed(title="Pullroom Add Log", description=f"{ctx.author.mention} (``{ctx.author.id}``) pulled {member.name}#{member.discriminator} (``{member.id}``) into the pullroom.\n\n**Reason:** {reason}", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                    embed3.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.display_avatar)
                    embed3.set_thumbnail(url=member.display_avatar)
                    await logging.send(embed=embed3)
                    await asyncio.sleep(3600)
                    if pullroom in user.roles:
                        await user.remove_roles(pullroomrole)

    @commands.command()
    @commands.guild_only()
    async def remove(self, ctx: commands.Context, member: discord.User, *, reason=""):
        pullroomrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "PULLROOMROLE"))
        logging = ctx.guild.get_channel(Configuration.getConfigVar(ctx.guild.id, "PULLROOMLOG"))
        modrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "MODROLE"))
        adminrole = ctx.guild.get_role(Configuration.getConfigVar(ctx.guild.id, "ADMINROLE"))
        roles = [modrole.id, adminrole.id]
        user_roles = [role.id for role in ctx.author.roles]
        verify = await self.bot.fetch_user(member.id)
        user = ctx.guild.get_member(verify.id)
        if reason == "":
            await ctx.send("Please specify a reason that you are removing the user from pullroom!")
            return
        if len(set(roles) & set(user_roles)) == 0:
            return
        if ctx.author.id == member.id:
            await ctx.send("Sorry, I am unable to help you to pull yourself out of the pullroom.")
        if pullroomrole not in user.roles:
            await ctx.send("This user already have had their role removed, likely manually by another moderator.")
            return
        if ctx.channel.type == discord.ChannelType.private_thread:
            await ctx.send(f"Removing ``{user.name}#{user.discriminator}`` (``{user.id}``) from the pullroom.")
            if pullroomrole is None:
                embed=discord.Embed(title="Unknown Role Error", description=f":warning: I was not able to remove {member.name}#{member.discriminator} (``{member.id}``)'s role upon archiving the thread. Please contact Ghoul in regards of this.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.display_avatar)
                await ctx.send(embed=embed)
            if pullroomrole in user.roles:
                try:
                    await user.remove_roles(pullroomrole)
                except discord.Forbidden as e:
                    embed=discord.Embed(title="Cannot remove Pullroom role", description=f":warning: I was not able to remove {member.name}#{member.discriminator} (``{member.id}``)'s role. Please contact Ghoul in regards of this.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                    embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.display_avatar)
                    await ctx.send(embed=embed)
                except discord.NotFound as e:
                    embed=discord.Embed(title="Unknown Member Error", description=f":warning: I was not able to add {member} to the pullroom. Please verify to ensure that the userID that you provided is correct.", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                    embed.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.display_avatar)
                    return await ctx.send(embed=embed)
                else: 
                    await ctx.channel.edit(archived=True, locked=True)
                    embed2=discord.Embed(title="Pullroom Remove Log", description=f"{ctx.author.mention} (``{ctx.author.id}``) pulled {member.name}#{member.discriminator} (``{member.id}``) out of the pullroom.\n\n**Reason:** {reason}", color=0xfff952,timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                    embed2.set_footer(text=f"Issued by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", icon_url=ctx.author.display_avatar)
                    embed2.set_thumbnail(url=member.display_avatar)
                    await logging.send(embed=embed2)
        else:
            await ctx.send("You need to use it in the thread to remove the user from the pullroom.")

        
async def setup(bot):
    await bot.add_cog(pullroom(bot))
