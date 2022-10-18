import discord
from discord.ext import commands
from discord import File
from discord import app_commands
from math import log, floor
import mysql.connector, easy_pil
from easy_pil import Editor, Font, Canvas

def human_format(number):
    units = ['', 'K', 'M', 'G', 'T', 'P']
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    thing = (number / k**magnitude, units[magnitude])
    if type(thing[0]) is float:
        value = thing[0]
        value = round(value, 1)
    def formatNumber(value):
        if value % 1 == 0:
            return int(value)
        else:
            return value
    return (f"{formatNumber(value)}{thing[1]}")

def connect():
    mydb = mysql.connector.connect(
    host="46.17.175.136",
    user="u456701538_MayumiData",
    password="Sakura12!",
    database="u456701538_MayumiSakura"
    )
    return mydb

def get_exp(author):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM Ranking WHERE UserID='{author.id}'")
    myresult = mycursor.fetchall()
    try:
        return int(myresult[0][1])
    except:
        return False

def add_user(author):
    mydb = connect()
    mycursor = mydb.cursor()
    #mycursor.execute(f"INSERT INTO Prefix (ServerID, Prefix) VALUES ('{guild.id}','ms.')")
    try:
        #try to add the prefix to the database with a paired guild id 
        mycursor.execute(f"INSERT INTO Ranking (UserID, Experience) VALUES ('{author.id}', '0')")
        #commit makes the change official
        mydb.commit()
    except:
        #serverid is unique and if a duplicate entry is given it will return this error
        print("duplicate entry or other.")

def add_exp(author, exp):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(f"UPDATE Ranking SET Experience='{exp}' WHERE UserID='{author.id}'")
    mydb.commit()
    print(f"added xp to {author}")

async def level_up(msg, exp):
    user = msg.author
    lvl = 0
    while True:
        if exp < ((50*(lvl**2))+(50*lvl)):
            break
        lvl+=1
    exp-=((50*((lvl-1)**2))+(50*(lvl-1)))
    if exp == 0:
        try:
            print(f"{msg.author} has leveled up")
            await msg.channel.send(f"{user.mention} has leveled up! **Level {lvl}**")
        except:
            pass

async def rank_card(msg, member, level, xp, total_xp):
    user=member
    status = str(user.status)
    pfp = user.avatar
    name = str(user)
    xp = int(xp)
    total_xp = int(total_xp)

    percentage = xp/total_xp
    percentage = percentage*100

    background = Editor("./Assets/RankCardBg.jpg")
    await user.avatar.save("./Assets/pfp.jpg")

    profile=Editor("./Assets/pfp.jpg").resize((150,150)).circle_image()
    poppins = Font.poppins(size=40)
    poppins_small = Font.poppins(size=30)

    square = Canvas((500,500), "#ff55aa")
    square = Editor(square)
    square.rotate(30, expand=True)

    background.paste(square.image, (600,-250))
    background.paste(profile.image, (30,30))

    if status == "offline":
        background.rectangle((140,150), width=25, height=25, fill="#777788", radius=20)
    elif status == "idle":
        background.rectangle((140,150), width=25, height=25, fill="#ffaa00", radius=20)
    elif status == "online":
        background.rectangle((140,150), width=25, height=25, fill="#55aa55", radius=20)
    elif status == "dnd":
        background.rectangle((140,150), width=25, height=25, fill="#ff6245", radius=20)
    else:
        await msg.channel.send(status)

    background.rectangle((30,220), width=650, height=40, fill="white", radius=20)
    background.bar((30,220), max_width=650, height=40, percentage=percentage, fill="#ff55aa", radius=20)
    background.text((200,40), f"{name}", font=poppins, color="white")

    background.rectangle((200, 100), width=350, height=2, fill="#ff55aa")
    background.text((200,130), f"Level: {level}   XP: {human_format(xp)}/{human_format(total_xp)}", font=poppins_small, color="white")

    file = File(fp=background.image_bytes, filename="./Assets/card.png")
    await msg.channel.send(file=file)

class Rank(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot == False:
            userxp = get_exp(msg.author)
            newexp = userxp+5
            if userxp == False:
                add_user(msg.author)
            add_exp(msg.author, newexp)
            await level_up(msg, newexp)

    @commands.command()
    async def rank(self, msg, member: discord.Member = None):
        if member == None:
            member = msg.author
            id = msg.author.id
            exp = get_exp(member)
            lvl = 0
            while True:
                if exp < ((50*(lvl**2))+(50*lvl)):
                    break
                lvl+=1
            exp-=((50*((lvl-1)**2))+(50*(lvl-1)))
            remaining = (200*((1/2)*lvl))
            await msg.channel.send(f"You are level: {lvl}")
            await rank_card(msg, member, lvl, exp, remaining)
        else:
            exp = exp = get_exp(member)
            lvl = 0
            while True:
                if exp < ((50*(lvl**2))+(50*lvl)):
                    break
                lvl+=1
            exp-=((50*((lvl-1)**2))+(50*(lvl-1)))
            remaining = (200*((1/2)*lvl))
            await msg.channel.send(f"{member.mention} is level: {lvl}")
            await rank_card(msg, member, lvl, exp, remaining)


    #error handling for rank command
    @rank.error
    async def rank_error(self, msg, error):
        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
                    await msg.send("that user does not have any xp")
        else:
            await msg.send("error, try again")
            print(error)

async def setup(client):
    await client.add_cog(Rank(client))
