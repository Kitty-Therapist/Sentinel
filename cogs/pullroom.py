import asyncio
import discord

from discord.ext import commands

class pullroom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Still some work to do, but work in progress so far.
    
    @commands.command()
    @commands.guild_only()
    async def pull(self, ctx: commands.Context, member: discord.User, *, reason=""):
        channel = ctx.guild.get_channel(969829406568771594)
        if reason is None:
            await ctx.send("Please specify a reason that you are pulling the user in!")
        else:
            verify = await self.bot.fetch_user(member.id)
            user = ctx.guild.get_member(verify.id)
            await ctx.send(f"Creating a pullroom thread for ``{user.name}#{user.discriminator}`` (``{user.id}``)")
            pullthread = await channel.create_thread(name=f"{user.name}-{user.discriminator} Pullroom", message=None, auto_archive_duration=60, type=None, reason = f"Pullroom request for {user.name}#{user.discriminator} ({user.id}) made by {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})", invitable = False, slowmode_delay = None)
            await pullthread.send(f"This is a pullroom test! {user.mention}")

    @commands.command()
    @commands.guild_only()
    async def remove(self, ctx: commands.Context, member: discord.User, *, reason=""):
        if reason is None:
            await ctx.send("Please specify a reason that you are removing the user!")
        else:
            verify = await self.bot.fetch_user(member.id)
            user = ctx.guild.get_member(verify.id)
            await ctx.send(f"Removing ``{user.name}`` from the pullroom.")
            await ctx.channel.edit(archived=True, locked=True)

        
async def setup(bot):
    await bot.add_cog(pullroom(bot))
