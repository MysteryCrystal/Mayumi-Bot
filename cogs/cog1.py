import discord
from discord.ext import commands
from discord import app_commands 

class cog1(commands.Cog):
    def __init__(self, client):
        self.client = client

        
    #app_commands(slash commands) take up to 24 hours to load into a server
    @app_commands.command(name = 'hilo', description='says hello')
    async def testy(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"I am working! I was made with Discord.py!", ephemeral = True) 

    @commands.command()
    async def new(self, msg):
        await msg.send("this is a new command")

    @commands.Cog.listener()
    async def on_message(self, msg):
        print(f"a message was sent in {msg}")
    
async def setup(client):
    await client.add_cog(cog1(client))
