import discord
from discord.ext import commands
from discord import app_commands 

class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client

    #features of the ticketting system:
    #complex or simple ticketting
    #ms.simpleticket will create an embed with a button to create a ticket channel
    #ms.complexticket will create an embed and the user will need to add buttons themselves
    #for each type of button a role will be assigned to be pinged/ or allowed to see messages and reply
    #logging channel to update and ping 
    #ms.setup creates a category with the logging channel in it
    



async def setup(client):
    await client.add_cog(Ticket(client))
