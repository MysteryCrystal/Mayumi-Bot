import discord
from discord.ext import commands
from discord import app_commands 

class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def role(self, msg, user : discord.Member, *, role : discord.Role):
        if role.position > msg.author.top_role.position: #if the role is above users top role it sends error
            return await msg.send(f"**:x: | That role is above {user.mention}'s top role!**") 
        if role in user.roles:
            await user.remove_roles(role) #removes the role if user already has
            await msg.send(f"Removed {role} from {user.mention}", delete_after=10)
        else:
            await user.add_roles(role) #adds role if not already has it
            await msg.send(f"Added {role} to {user.mention}", delete_after=10) 

    @commands.command()
    async def roleinfo(self, msg, role: discord.Role):
        if role is None:
            await msg.channel.send("no role given")      
            return
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(description=role.mention, color=(0x2af7fc))
        embed.set_author(name=str(role), icon_url=msg.guild.icon)
        embed.set_thumbnail(url=msg.guild.icon)
        embed.add_field(name="Color", value=role.color)
        embed.add_field(name="Created At", value=role.created_at.strftime(date_format))
        embed.add_field(name="Used By", value=len(role.members))
        embed.add_field(name="Rank", value=role.position)
        embed.add_field(name="Mentionable", value=role.mentionable)
        embed.add_field(name="Tags", value=role.tags)
        embed.set_footer(text='ID: ' + str(role.id))
        return await msg.send(embed=embed)


#autobotrole

async def setup(client):
    await client.add_cog(Roles(client))
