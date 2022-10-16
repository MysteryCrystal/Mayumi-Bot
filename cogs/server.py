import discord
from discord.ext import commands
from discord import app_commands 

class Server(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def serverinfo(self, msg):
        guild= msg.guild
        description= guild.description
        owner = guild.owner
        count = guild.member_count
        icon = guild.icon   
        guildid = guild.id
        print(guild)
        print(description)
        print(owner)
        print(count)
        print(icon)
        print(guildid)
async def setup(client):
    await client.add_cog(Server(client))
