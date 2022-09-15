import discord
from discord.ext import commands
from discord import app_commands 

class servercount(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(title="∭︱Server Count", description="the server count went up!", colour=0x00FF00)
        embed.add_field(name="Server Count", value=len(self.client.guilds), inline=True)
        channel = self.client.get_channel(int(941300241351716864))
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        embed = discord.Embed(title="∭︱Server Count", description="the server count went down!", colour=0xFF0000)
        embed.add_field(name="Server Count", value=len(self.client.guilds), inline=True)
        channel = self.client.get_channel(int(941300241351716864))
        await channel.send(embed=embed)

async def setup(client):
    await client.add_cog(servercount(client))
