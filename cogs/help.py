import discord, urllib
from discord.ext import commands
from discord import app_commands 

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group()
    async def help(self, msg):
        if msg.invoked_subcommand is None:  
            em= discord.Embed(title="Help",colour=0x2af7fc)
            em.add_field(name="info", value="`.help info`", inline=False)
            em.add_field(name="Tickets", value="`.help tickets`", inline=False)
            em.set_footer(text=". represents the prefix")
            pfp = self.client.user.avatar
            em.set_thumbnail(url=pfp)
            await msg.channel.send(embed=em)
        else:
            pass

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.mentions[0]==self.user:
          description="Hi, my name is Mayumi Sakura², you can call me Mayu! I am still a work in progress right now but I am here to simplify the life of server owners and help you have as little bots in one server at once while still having the same amount (or more) of features! More features are being added every day!"
          servercount=str(len(self.guilds))
          pfp = self.user.avatar_url
          owner="Mystery_C#5296"
          prefix="`ms.`"
          link="[Website link](https://www.mayumisakura.com/)"
          linkk = urllib.parse.unquote_plus('https://discord.com/api/oauth2/authorize?client_id=794545370927595531&permissions=8&redirect_uri=https%3A%2F%2Fmayumisakura.com%2F&scope=bot')
          link2=f"[add me to your server!]({linkk})"
          embed = discord.Embed(title="Mayumi Sakura²", description=description,color=(0x2af7fc))
          embed.set_thumbnail(url=pfp)
          embed.add_field(name="Owner", value=owner, inline=True)
          embed.add_field(name="Server Count", value=servercount, inline=True)
          embed.add_field(name="Prefix", value=prefix, inline=True)
          embed.add_field(name="Website", value=link, inline=True)
          embed.add_field(name="Invite", value=link2, inline=True)
          await msg.channel.send(embed=embed)

async def setup(client):
    await client.add_cog(Help(client))
