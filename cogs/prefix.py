import discord
from discord.ext import commands
#slash commands
from discord import app_commands 
#allows for connecting to website database
import mysql.connector

#function to connect to website database using credentials
def connect():
    mydb = mysql.connector.connect(
    host="46.17.175.136",
    user="u456701538_MayumiData",
    password="Sakura12!",
    database="u456701538_MayumiSakura"
    )
    return mydb

def get_prefix(message):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM Prefix WHERE ServerID='{message.guild.id}'")
    myresult = mycursor.fetchall()
    #print(myresult[0][1])
    return myresult[0][1]

class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    #runs when the bot joins a server (needs the guild parameter)
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        #connect to database
        mydb=connect()
        mycursor = mydb.cursor()
        try:
            #try to add the prefix to the database with a paired guild id 
            mycursor.execute(f"INSERT INTO Prefix (ServerID, Prefix) VALUES ('{guild.id}','ms.')")
            #commit makes the change official
            mydb.commit()
        except:
            #serverid is unique and if a duplicate entry is given it will return this error
            print("duplicate entry or other.")

    #when the bot leaves a server
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        mydb=connect()
        mycursor = mydb.cursor()
        serverid = guild.id
        try:
            #try delete the prefix
            mycursor.execute(f"DELETE FROM Prefix WHERE ServerID='{serverid}'")
            mydb.commit()
        except:
            #failure to delete means it wasn't there in the first place (shouldn't happen)
            print("failure to delete")
        print(mycursor.rowcount, "record(s) deleted")

    #command to change prefix (takes the message and an optional prefix parameter)
    @commands.command()
    async def prefix(self, msg, prefix):
        mydb=connect()
        mycursor = mydb.cursor()
        serverid = msg.guild.id
        #update the prefix 
        mycursor.execute(f"UPDATE Prefix SET Prefix='{prefix}' WHERE ServerID='{serverid}'")
        mydb.commit()
        #send an embed confirming the change
        embed= discord.Embed(title="Prefix", description=f"Your prefix has been changed to {prefix}", colour=0x2af7fc)
        await msg.send(embed=embed)

    @prefix.error
    async def flip_error(self, msg, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await msg.send(f"your prefix is {get_prefix(msg)}")
    

async def setup(client):
    await client.add_cog(Prefix(client))
