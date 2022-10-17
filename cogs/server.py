import discord
from discord.ext import commands
from discord import app_commands 

class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def serverinfo(self, msg):
        guild= msg.guild
        embed = discord.Embed(
            title = guild,
            description = guild.description,
            color = 0x2af7fc
        )
        embed.set_thumbnail(url=guild.icon )
        embed.add_field(name = "owner", value = guild.owner, inline = True)
        embed.add_field(name = "serverid", value = guild.id, inline = True)
        embed.add_field(name = "members", value = guild.member_count, inline = True)
        embed.set_footer(text=f"id={guild.id}")
        await msg.send(embed=embed)

async def setup(client):
    await client.add_cog(User(client))
