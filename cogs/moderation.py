import discord, datetime
from discord.ext import commands
from discord import app_commands 

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, msg, user: discord.Member, *, reason = None):
        ban= discord.Embed(title=f'A moderation action has been performed!', description='', color=(0x2af7fc))
        ban.add_field(name='Moderator Name:', value=f'`{msg.author}`', inline=True)
        ban.add_field(name='Moderator ID:', value=f'`{msg.author.id}`', inline=True)
        ban.add_field(name='Action Performed:', value='`Ban`', inline=True)
        ban.timestamp = datetime.datetime.utcnow()

        await msg.send(embed=ban)
        await user.ban(reason = reason)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unban(self, msg, id: int):
        user = await self.client.fetch_user(id)
        await msg.guild.unban(user)

        unban= discord.Embed(title=f'A moderation action has been performed!', description='', color=(0x2af7fc))
        unban.add_field(name='Moderator Name:', value=f'`{msg.author}`', inline=True)
        unban.add_field(name='Moderator ID:', value=f'`{msg.author.id}`', inline=True)
        unban.add_field(name='Action Performed:', value='`UnBan`', inline=True)
        unban.timestamp = datetime.datetime.utcnow()

        await msg.send(embed=unban)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def kick(self,msg, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        kick= discord.Embed(title=f'A moderation action has been performed!', description='', color=(0x2af7fc))
        kick.add_field(name='Moderator Name:', value=f'`{msg.author}`', inline=True)
        kick.add_field(name='Moderator ID:', value=f'`{msg.author.id}`', inline=True)
        kick.add_field(name='Action Performed:', value='`Kick`', inline=True)
        kick.timestamp = datetime.datetime.utcnow()

        await msg.send(embed=kick)
        await msg.message.delete()
        await msg.channel.send(embed=kick)
        kick = discord.Embed(title=f":boot: You Have Been Kicked!", description=f"From: {msg.guild.name}\nReason: {reason}")
        await user.send(embed=kick)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, msg, seconds):
        try:
            await msg.channel.edit(slowmode_delay=int(seconds))
            await msg.send(f"Set the slowmode delay in this channel to {seconds} seconds!")
        except:
            await msg.channel.send("Failed to set cooldown, have all parameters been met?")

async def setup(client):
    await client.add_cog(Moderation(client))
