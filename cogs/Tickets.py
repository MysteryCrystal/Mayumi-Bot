from curses import BUTTON1_PRESSED
from operator import truediv
from socket import timeout
from unicodedata import category
import discord
from discord import File
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio, os, json
from discord.ui import Button, View


async def close(self, channel):
    with open('./Assets/ticket.json') as f:
        data = json.load(f)

    if channel.id in data[f"{channel.guild.id}"]["ticket-channel-ids"]:

        channel_id = channel.id

        await channel.delete()

        data[f"{channel.guild.id}"]["ticket-counter"] -= 1

        index = data[f"{channel.guild.id}"]["ticket-channel-ids"].index(channel_id)
        del data[f"{channel.guild.id}"]["ticket-channel-ids"][index]

        with open('./Assets/ticket.json', 'w') as f:
            json.dump(data, f, indent=4)

async def new(self, channel, author):
    message_content = "Please wait, we will be with you shortly!"
    with open("./Assets/ticket.json") as f:
        data = json.load(f)

    ticket_number = int(data[f"{channel.guild.id}"]["ticket-counter"])
    ticket_number += 1

    ticket_channel = await channel.guild.create_text_channel("ticket-{}".format(ticket_number), category=channel.category)
    await ticket_channel.set_permissions(channel.guild.get_role(channel.guild.id), send_messages=False, read_messages=False)

    for role_id in data[f"{channel.guild.id}"]["valid-roles"]:
        role = channel.guild.get_role(role_id)

        await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
    
    await ticket_channel.set_permissions(author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

    em = discord.Embed(title="New ticket from {}#{}".format(author.name, author.discriminator), description= "{}".format(message_content), color=0x2af7fc)


    async def buttonCallback(interaction):
        async def buttonCallbackclose(interaction):
            with open("./Assets/ticket.json") as f:
                data = json.load(f)
            logchannel = data[f"{interaction.message.guild.id}"]["log-channel"]
            ticketamount = data[f"{interaction.message.guild.id}"]["ticket-counter"]
            if logchannel != 0:
                logchannel=self.client.get_channel(logchannel)
                embed = discord.Embed(title="Ticket closed", description=f"closed ticket #{ticketamount} by {interaction.user}", color=0x2af7fc)
                await logchannel.send(embed=embed)
            await close(self, interaction.channel)

        async def buttonCallbackcancel(interaction):
            await interaction.message.delete()

        em = discord.Embed(title="Ticket", description= "Are you sure you want to close this ticket", color=0x2af7fc)

        button2 = Button(label='Close', style=discord.ButtonStyle.danger)
        button3 = Button(label='Cancel', style=discord.ButtonStyle.gray)

        button2.callback = buttonCallbackclose
        button3.callback = buttonCallbackcancel


        view2=View()
        view2.add_item(button2)
        view2.add_item(button3)

        message = await ticket_channel.send(embed=em, view=view2)
    
    button1 = Button(label='Close ticket', style=discord.ButtonStyle.danger, emoji="🔒")
    button1.callback = buttonCallback 
    view=View()
    view.add_item(button1)
    await ticket_channel.send(embed=em, view=view)

    pinged_msg_content = ""
    non_mentionable_roles = []

    if data[f"{channel.guild.id}"]["pinged-roles"] != []:

        for role_id in data[f"{channel.guild.id}"]["pinged-roles"]:
            role = channel.guild.get_role(role_id)

            pinged_msg_content += role.mention
            pinged_msg_content += " "

            if role.mentionable:
                pass
            else:
                await role.edit(mentionable=True)
                non_mentionable_roles.append(role)
        
        await ticket_channel.send(pinged_msg_content)

        for role in non_mentionable_roles:
            await role.edit(mentionable=False)
    
    data[f"{channel.guild.id}"]["ticket-channel-ids"].append(ticket_channel.id)

    data[f"{channel.guild.id}"]["ticket-counter"] = int(ticket_number)
    with open("./Assets/ticket.json", 'w') as f:
        json.dump(data, f, indent=4)

    return (ticket_channel)

class ticket(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    #features of the ticketting system:
    #complex or simple ticketting
    #ms.simpleticket will create an embed with a button to create a ticket channel
    #ms.complexticket will create an embed and the user will need to add buttons themselves
    #for each type of button a role will be assigned to be pinged/ or allowed to see messages and reply
    #logging channel to update and ping 
    #ms.setup creates a category with the logging channel in it
    


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("./Assets/ticket.json") as f:
            data = json.load(f)

        if not f"{guild.id}" in data:
            data[f"{guild.id}"] = {}
            data[f"{guild.id}"]["ticket-counter"] = 0
            data[f"{guild.id}"]["valid-roles"] = []
            data[f"{guild.id}"]["pinged-roles"] = []
            data[f"{guild.id}"]["ticket-channel-ids"] = []
            data[f"{guild.id}"]["verified-roles"] = []
            data[f"{guild.id}"]["log-channel"] = 0

        with open("./Assets/ticket.json", "w") as f:
            json.dump(data, f, indent=4)

    @commands.command()
    async def new(self, ctx, *, args = None):

        await self.client.wait_until_ready()

        if args == None:
            message_content = "Please wait, we will be with you shortly!"
        
        else:
            message_content = "".join(args)

        with open("./Assets/ticket.json") as f:
            data = json.load(f)

        ticket_number = int(data[f"{ctx.guild.id}"]["ticket-counter"])
        ticket_number += 1

        ticket_channel = await ctx.guild.create_text_channel("ticket-{}".format(ticket_number))
        await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)

        for role_id in data[f"{ctx.guild.id}"]["valid-roles"]:
            role = ctx.guild.get_role(role_id)

            await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
        
        await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

        em = discord.Embed(title="New ticket from {}#{}".format(ctx.author.name, ctx.author.discriminator), description= "{}".format(message_content), color=0x2af7fc)

        await ticket_channel.send(embed=em)

        pinged_msg_content = ""
        non_mentionable_roles = []

        if data[f"{ctx.guild.id}"]["pinged-roles"] != []:

            for role_id in data[f"{ctx.guild.id}"]["pinged-roles"]:
                role = ctx.guild.get_role(role_id)

                pinged_msg_content += role.mention
                pinged_msg_content += " "

                if role.mentionable:
                    pass
                else:
                    await role.edit(mentionable=True)
                    non_mentionable_roles.append(role)
            
            await ticket_channel.send(pinged_msg_content)

            for role in non_mentionable_roles:
                await role.edit(mentionable=False)
        
        data[f"{ctx.guild.id}"]["ticket-channel-ids"].append(ticket_channel.id)

        data[f"{ctx.guild.id}"]["ticket-counter"] = int(ticket_number)
        with open("./Assets/ticket.json", 'w') as f:
            json.dump(data, f, indent=4)
        
        created_em = discord.Embed(title="Tickets", description="Your ticket has been created at {}".format(ticket_channel.mention), color=0x2af7fc)
        
        await ctx.send(embed=created_em)


    @commands.command()
    async def close(self, ctx):
        with open('./Assets/ticket.json') as f:
            data = json.load(f)

        if ctx.channel.id in data[f"{ctx.guild.id}"]["ticket-channel-ids"]:

            channel_id = ctx.channel.id

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "close"

            try:

                em = discord.Embed(title=" Tickets", description="Are you sure you want to close this ticket? Reply with `close` if you are sure.", color=0x2af7fc)
            
                await ctx.send(embed=em)
                await self.client.wait_for('message', check=check, timeout=60)
                await ctx.channel.delete()

                data[f"{ctx.guild.id}"]["ticket-counter"] -= 1

                index = data[f"{ctx.guild.id}"]["ticket-channel-ids"].index(channel_id)
                del data[f"{ctx.guild.id}"]["ticket-channel-ids"][index]

                with open('./Assets/ticket.json', 'w') as f:
                    json.dump(data, f, indent=4)
            
            except asyncio.TimeoutError:
                em = discord.Embed(title=" Tickets", description="You have run out of time to close this ticket. Please run the command again.", color=0x2af7fc)
                await ctx.send(embed=em)


    @commands.command()
    async def addaccess(self, ctx, role_id=None):

        with open('./Assets/ticket.json') as f:
            data = json.load(f)
        
        valid_user = False

        for role_id in data[f"{ctx.guild.id}"]["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
        
        if valid_user or ctx.author.guild_permissions.administrator:
            role_id = int(role_id)

            if role_id not in data[f"{ctx.guild.id}"]["valid-roles"]:

                try:
                    role = ctx.guild.get_role(role_id)

                    with open("./Assets/ticket.json") as f:
                        data = json.load(f)

                    data[f"{ctx.guild.id}"]["valid-roles"].append(role_id)

                    with open('./Assets/ticket.json', 'w') as f:
                        json.dump(data, f, indent=4)
                    
                    em = discord.Embed(title=" Tickets", description="You have successfully added `{}` to the list of roles with access to tickets.".format(role.name), color=0x2af7fc)

                    await ctx.send(embed=em)

                except:
                    em = discord.Embed(title=" Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                    await ctx.send(embed=em)
            
            else:
                em = discord.Embed(title=" Tickets", description="That role already has access to tickets!", color=0x2af7fc)
                await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title=" Tickets", description="Sorry, you don't have permission to run that command.", color=0x2af7fc)
            await ctx.send(embed=em)


    @commands.command()
    async def delaccess(self, ctx, role_id=None):
        with open('./Assets/ticket.json') as f:
            data = json.load(f)
        
        valid_user = False

        for role_id in data[f"{ctx.guild.id}"]["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass

        if valid_user or ctx.author.guild_permissions.administrator:

            try:
                role_id = int(role_id)
                role = ctx.guild.get_role(role_id)

                with open("./Assets/ticket.json") as f:
                    data = json.load(f)

                valid_roles = data[f"{ctx.guild.id}"]["valid-roles"]

                if role_id in valid_roles:
                    index = valid_roles.index(role_id)

                    del valid_roles[index]

                    data[f"{ctx.guild.id}"]["valid-roles"] = valid_roles

                    with open('./Assets/ticket.json', 'w') as f:
                        json.dump(data, f, indent=4)

                    em = discord.Embed(title=" Tickets", description="You have successfully removed `{}` from the list of roles with access to tickets.".format(role.name), color=0x2af7fc)

                    await ctx.send(embed=em)
                
                else:
                    
                    em = discord.Embed(title=" Tickets", description="That role already doesn't have access to tickets!", color=0x2af7fc)
                    await ctx.send(embed=em)

            except:
                em = discord.Embed(title=" Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title=" Tickets", description="Sorry, you don't have permission to run that command.", color=0x2af7fc)
            await ctx.send(embed=em)

    @commands.command()
    async def addpingedrole(ctx, role_id=None):

        with open('./Assets/ticket.json') as f:
            data = json.load(f)
        
        valid_user = False

        for role_id in data[f"{ctx.guild.id}"]["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
        
        if valid_user or ctx.author.guild_permissions.administrator:

            role_id = int(role_id)

            if role_id not in data[f"{ctx.guild.id}"]["pinged-roles"]:

                try:
                    role = ctx.guild.get_role(role_id)

                    with open("./Assets/ticket.json") as f:
                        data = json.load(f)

                    data[f"{ctx.guild.id}"]["pinged-roles"].append(role_id)

                    with open('./Assets/ticket.json', 'w') as f:
                        json.dump(data, f, indent=4)

                    em = discord.Embed(title=" Tickets", description="You have successfully added `{}` to the list of roles that get pinged when new tickets are created!".format(role.name), color=0x2af7fc)

                    await ctx.send(embed=em)

                except:
                    em = discord.Embed(title=" Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                    await ctx.send(embed=em)
                
            else:
                em = discord.Embed(title=" Tickets", description="That role already receives pings when tickets are created.", color=0x2af7fc)
                await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title=" Tickets", description="Sorry, you don't have permission to run that command.", color=0x2af7fc)
            await ctx.send(embed=em)


    @commands.command()
    async def delpingedrole(self, ctx, role_id=None):

        with open('./Assets/ticket.json') as f:
            data = json.load(f)
        
        valid_user = False

        for role_id in data[f"{ctx.guild.id}"]["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
        
        if valid_user or ctx.author.guild_permissions.administrator:

            try:
                role_id = int(role_id)
                role = ctx.guild.get_role(role_id)

                with open("./Assets/ticket.json") as f:
                    data = json.load(f)

                pinged_roles = data[f"{ctx.guild.id}"]["pinged-roles"]

                if role_id in pinged_roles:
                    index = pinged_roles.index(role_id)

                    del pinged_roles[index]

                    data[f"{ctx.guild.id}"]["pinged-roles"] = pinged_roles

                    with open('./Assets/ticket.json', 'w') as f:
                        json.dump(data, f, indent=4)

                    em = discord.Embed(title=" Tickets", description="You have successfully removed `{}` from the list of roles that get pinged when new tickets are created.".format(role.name), color=0x2af7fc)
                    await ctx.send(embed=em)
                
                else:
                    em = discord.Embed(title=" Tickets", description="That role already isn't getting pinged when new tickets are created!", color=0x2af7fc)
                    await ctx.send(embed=em)

            except:
                em = discord.Embed(title=" Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title=" Tickets", description="Sorry, you don't have permission to run that command.", color=0x2af7fc)
            await ctx.send(embed=em)


    @commands.command()
    @has_permissions(administrator=True)
    async def addadminrole(ctx, role_id=None):

        try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)

            with open("./Assets/ticket.json") as f:
                data = json.load(f)

            data[f"{ctx.guild.id}"]["verified-roles"].append(role_id)

            with open('./Assets/ticket.json', 'w') as f:
                json.dump(data, f, indent=4)
            
            em = discord.Embed(title=" Tickets", description="You have successfully added `{}` to the list of roles that can run admin-level commands!".format(role.name), color=0x2af7fc)
            await ctx.send(embed=em)

        except:
            em = discord.Embed(title=" Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
            await ctx.send(embed=em)

    @commands.command()
    @has_permissions(administrator=True)
    async def deladminrole(ctx, role_id=None):
        try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)

            with open("./Assets/ticket.json") as f:
                data = json.load(f)

            admin_roles = data[f"{ctx.guild.id}"]["verified-roles"]

            if role_id in admin_roles:
                index = admin_roles.index(role_id)

                del admin_roles[index]

                data[f"{ctx.guild.id}"]["verified-roles"] = admin_roles

                with open('./Assets/ticket.json', 'w') as f:
                    json.dump(data, f, indent=4)
                
                em = discord.Embed(title=" Tickets", description="You have successfully removed `{}` from the list of roles that get pinged when new tickets are created.".format(role.name), color=0x2af7fc)

                await ctx.send(embed=em)
            
            else:
                em = discord.Embed(title=" Tickets", description="That role isn't getting pinged when new tickets are created!", color=0x2af7fc)
                await ctx.send(embed=em)

        except:
            em = discord.Embed(title=" Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
            await ctx.send(embed=em)

    @commands.command(aliases=['create'])
    async def createticket(self, msg):
        em = discord.Embed(title=" Tickets", description="React to create a ticket", color=0x2af7fc)

        button1 = Button(label='Create ticket', style=discord.ButtonStyle.gray, emoji="📩")

        #async def buttonCallback(interaction):
            #channel = await new(self, msg.channel, msg.author)
            #await interaction.response.send_message(f"New ticket created at {channel.mention}")

        
        #button1.callback = buttonCallback

        view=View()
        view.add_item(button1)
        await msg.channel.send(embed=em, view=view)
        await msg.message.delete()

    @commands.command(aliases=["ticketlogs"])
    async def ticketlog(self, msg):
        with open("./Assets/ticket.json") as f:
                data = json.load(f)
        
        if data[f"{msg.guild.id}"]["log-channel"] == 0:
            data[f"{msg.guild.id}"]["log-channel"] = msg.channel.id
            with open('./Assets/ticket.json', 'w') as f:
                json.dump(data, f, indent=4)
            await msg.channel.send("enabled logging")
        elif data[f"{msg.guild.id}"]["log-channel"] != 0:
            data[f"{msg.guild.id}"]["log-channel"] = 0
            with open('./Assets/ticket.json', 'w') as f:
                json.dump(data, f, indent=4)

            await msg.channel.send("disabled logging")
        else:
            pass
        

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        embed_content_in_dict = interaction.message.embeds[0].to_dict()
        guild = interaction.guild
        with open("./Assets/ticket.json") as f:
            data = json.load(f)

        if data[f"{guild.id}"]:
            if embed_content_in_dict["description"] == "React to create a ticket":
                channel = await new(self, interaction.channel, interaction.user)
                msg = await interaction.message.channel.send(f"New ticket created at {channel.mention}")
                with open("./Assets/ticket.json") as f:
                    data = json.load(f)
                ticketamount = data[f"{guild.id}"]["ticket-counter"]
                logchannel = data[f"{channel.guild.id}"]["log-channel"]
                if logchannel != 0:
                    logchannel=self.client.get_channel(logchannel)
                    embed = discord.Embed(title="Ticket opened", description=f"opened ticket #{ticketamount} by {interaction.user}", color=0x2af7fc)
                    try:
                        await logchannel.send(embed=embed)
                    except:
                        pass
                await asyncio.sleep(5)
                await msg.delete()
            else:
                pass
        else:
            pass
    
async def setup(client):
    await client.add_cog(ticket(client))