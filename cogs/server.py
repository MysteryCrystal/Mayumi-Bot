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
        embed = discord.Embed(
            title = guild, 
            description = description,
            color = 0x2af7fc
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name = "owner", value = owner, inline = True)
        embed.add_field(name = "serverid", value = guildid, inline = True)
        embed.add_field(name = "members", value = count, inline = True)
        embed.set_footer(text=f"id={guildid}")
        await msg.send(embed=embed)

async def setup(client):
    await client.add_cog(Server(client))
