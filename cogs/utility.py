import discord, datetime, random
from discord.ext import commands
from discord import app_commands 

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, message, amount=6):
        await message.channel.purge(limit=amount)

    @commands.command()
    async def pp(self, msg, user : discord.Member):
        if user is None:
            user = msg.author
        elif user.id == 794545370927595531:
            embed = discord.Embed(title=f"{user.name}'s PP Size!",description=f"I dont have that!", color=0x2af7fc)
            await msg.channel.send(embed=embed)
            return
        else:
            number = int(random.randint(1,7))
        ppshaft = "="*number
        embed = discord.Embed(title=f"{user.name}'s PP Size!",description=f"8{ppshaft}D", color=0x2af7fc)
        await msg.channel.send(embed=embed)

async def setup(client):
    await client.add_cog(Utility(client))
