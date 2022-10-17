import discord
from discord.ext import commands
from discord import app_commands 

class Server(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def userinfo(self, msg, user: discord.Member):
        if user is None:
            user = msg.author      
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(description=user.mention, color=(0x2af7fc))
        embed.set_author(name=str(user), icon_url=user.avatar)
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(msg.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user)+1))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        embed.add_field(name="Guild permissions", value=perm_string, inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        return await msg.send(embed=embed)

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, member:discord.Member):
        await ctx.send(member.avatar)

async def setup(client):
    await client.add_cog(Server(client))
