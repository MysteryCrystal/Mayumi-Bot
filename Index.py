import discord
from discord.ext import commands
from discord import app_commands 
import os


class client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = "m.", intents = discord.Intents.all())
        self.synced = False 

    async def load_extensions(self):
        #os.listdir gets all the files in the path
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: 
            await tree.sync(guild = discord.Object(id=920576397704040488)) 
            self.synced = True
        await self.load_extensions()
        print(f"We have logged in as {self.user}.")


aclient = client()

try:
    tree = app_commands.CommandTree(aclient)
except:
    tree=aclient.tree

@tree.command(guild = discord.Object(id=920576397704040488), name = 'hey', description='says hello')
async def testy(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey there!", ephemeral = True) 



aclient.run('Nzk0NTQ1MzcwOTI3NTk1NTMx.X-8YCg.pjWa4SGpQ69if-W2Y3xdq62hFXQ')





