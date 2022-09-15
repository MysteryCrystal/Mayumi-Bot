import asyncio
import discord
from discord.ext import commands
from discord import app_commands 
import os
import mysql.connector

def get_prefix(client, message):
    mydb = mysql.connector.connect(
    host="46.17.175.136",
    user="u456701538_MayumiData",
    password="Sakura12!",
    database="u456701538_MayumiSakura"
    )
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM Prefix WHERE ServerID='{message.guild.id}'")
    myresult = mycursor.fetchall()
    #print(myresult[0][1])
    return myresult[0][1]

class client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = get_prefix, intents = discord.Intents.all())
        self.synced = False 


    async def load_extensions(self):
        #os.listdir gets all the files in the path
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def on_ready(self):
        if not self.synced: 
            await tree.sync(guild = discord.Object(id=920576397704040488)) 
            self.synced = True
        print(f"We have logged in as {self.user}.")

    async def on_message(self, msg):
        #print(f"a message was sent in {msg.channel}")
        #on_message blocks the bot from taking messages as commands
        #this is why you process them as commands after
        await self.process_commands(msg)


aclient = client()
aclient.remove_command("help")

try:
    tree = app_commands.CommandTree(aclient)
except:
    tree=aclient.tree

@tree.command(guild = discord.Object(id=920576397704040488), name = 'hey', description='says hello')
async def testy(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey there!", ephemeral = True) 


asyncio.run(aclient.load_extensions())
aclient.run('Nzk0NTQ1MzcwOTI3NTk1NTMx.X-8YCg.pjWa4SGpQ69if-W2Y3xdq62hFXQ')





