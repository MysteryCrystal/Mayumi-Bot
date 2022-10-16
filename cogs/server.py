import discord
from discord.ext import commands
from discord import app_commands 

class Server(commands.Cog):
    def __init__(self, client):
        self.client = client

async def setup(client):
    await client.add_cog(Server(client))
