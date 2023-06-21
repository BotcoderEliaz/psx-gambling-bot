import string

username = "henrymistert2" # The Username Of The Account Running The LUA Script (Run This Before The Lua Script)
workspacefolder = "C:/Users/henry/AppData/Local/Packages/ROBLOXCORPORATION.ROBLOX_55nm5eh3cm0pr/AC/workspace" # The Workspace Folder Of Your Executor
rainwebhook = "https://discord.com/api/webhooks/1107300723194073203/WPtU-2a2E0Qksm8-PrpPQS76Pzi7NpvL8zGkbnFSJOLziREjLosHzh5VAv5jqCCWL-TF"
withwebhook = "https://discord.com/api/webhooks/1107300770447114353/wToJ97omKRDvPHFVJX54pkXzT139asp93ND30gN9465Zb7GS8s89gKkSnm1o7QnvvaIW"
depowebhook = "https://discord.com/api/webhooks/1107300675278348338/Io7fmyZcirT0BNChCfXdNmMnetndKh9KK7N-bkE-lB-0EyVkA9WSnaNpMZuW3XF5WiU1"
crashwebhook = "https://discord.com/api/webhooks/1107300629027758130/LoD-BIWAB2qG_x1FC8VMkDa6cIoRFGfGApemmJHxTFCdHUiWCvxtij8eyJMAXFoSOHss"
import discord
from discord import app_commands
from discord.ext import commands
import json
import random
import time
import asyncio
import websockets
import threading
import os
from enum import Enum
from discord import Button, ButtonStyle
import requests
class CoinSide(Enum):
    Heads = "Heads"
    Tails = "Tails"
class RPSSide(Enum):
    Rock = "Rock"
    Paper = "Paper"
    Scissors = "Scissors"

rpsgames = []
codes = []
words = ['apple', 'banana', 'fruit', 'car', 'base', 'good', 'life', 'up', 'shift', 'left', 'down', 'code']
rains = []
crash = {
    "FinishTime": 0,
    "Multi": 0,
    "Users": []
}
workspacefolder += "/gamble" # Ignore
os.makedirs(workspacefolder, exist_ok=True)
temp = open(f"{workspacefolder}/withdraws.txt", "w")
temp.close()
temp = open(f"{workspacefolder}/deposits.txt", "w")
temp.close()
def suffix_to_int(s):
    suffixes = {
        'k': 3,
        'm': 6,
        'b': 9,
        't': 12
    }

    suffix = s[-1].lower()
    if suffix in suffixes:
        num = float(s[:-1]) * 10 ** suffixes[suffix]
    else:
        num = float(s)

    return int(num)
def readdata() :
    with open("userdata.json", "r") as infile :
        # Load the data from the file into a dictionary
        userdata = json.load(infile)

        # Close the file

        infile.close()
        return (userdata)


def writedata(data) :
    with open("userdata.json", "w") as outfile :
        json.dump(data, outfile)
        outfile.close()

def register_user(uid):
    data = readdata()
    data["gems"].append([uid, 0])
    writedata(data)

def is_registered(uid):
    data = readdata()
    found = False
    for user in data['gems']:
        if user[0] == uid:
            found = True
    return found
def get_gems(uid):
    data = readdata()
    gems = 0
    for user in data['gems']:
        if user[0] == uid:
            gems = user[1]
    return gems
def set_gems(uid, gems):
    data = readdata()
    count = 0
    for user in data['gems']:
        if user[0] == uid:
            data['gems'][count][1] = gems
        count += 1
    writedata(data)
def add_gems(uid, gems):
    set_gems(uid, get_gems(uid) + gems)

def subtract_gems(uid, gems) :
    set_gems(uid, get_gems(uid) - gems)
add_gems("123", 20)
def test_code(code, gems):
    count = 0
    for item in codes:
        if item[1] == code:
            add_gems(item[0], gems)
            message = {
                "content" : f"<@{item[0]}> Deposited {gems}!"
            }
            requests.post(url=depowebhook,json=message)
            codes.remove(item)
        count+=1

def send_message(message):
    f = open(f"{workspacefolder}/withdraws.txt", "a")
    f.write(f"{message}\n")
    f.close()

def background_function():
    while 1:
        time.sleep(1)
        f = open(f"{workspacefolder}/deposits.txt", "r")
        lines = f.readlines()
        f.close()
        for message2 in lines:
            message = message2.replace("\n", "")
            msg = message.split(",")
            code = msg[0]
            gems = int(msg[1])
            test_code(code=code, gems=gems)
        f = open(f"{workspacefolder}/deposits.txt", "w")
        f.writelines("")
background_thread = threading.Thread(target=background_function)
background_thread.start()
bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())
def crash_multi():
    multi = 0.1
    crashc = 3.5
    while 1 :
        random_num = random.randint(0, 100)
        if random_num <= crashc :
            break
        else :
            multi += 0.1
            crashc += 1
    return round(multi, 1)
def add_suffix(inte):
    gems = inte
    if gems >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
        gems_formatted = f"{gems / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
    elif gems >= 1000000000 :  # if gems are greater than or equal to 1 billion
        gems_formatted = f"{gems / 1000000000:.1f}b"  # display gems in billions with one decimal point
    elif gems >= 1000000 :  # if gems are greater than or equal to 1 million
        gems_formatted = f"{gems / 1000000:.1f}m"  # display gems in millions with one decimal point
    elif gems >= 1000 :  # if gems are greater than or equal to 1 thousand
        gems_formatted = f"{gems / 1000:.1f}k"  # display gems in thousands with one decimal point
    else :  # if gems are less than 1 thousand
        gems_formatted = str(gems)  # display gems as is
    return gems_formatted
def update_crash_game():
    global crash
    while 1:
        multi = crash_multi()
        crash = {
            "FinishTime": round(time.time() + 15),
            "Multi": multi,
            "Users": [],
            "MessageID": ""
        }
        message = {
            "content" : f"",
            "embeds" : [
                {
                    "title" : ":rocket: Crash",
                    "description" : "A New Game Of Crash Has Started! Type /join-crash With The Amount Of Gems To Bet To Join!",
                    "color" : 5814783,
                    "fields" : [
                        {
                            "name" : "Details",
                            "value" : f":rocket: **Crashes:** <t:{crash['FinishTime']}:R>\n:exclamation: **Participants:** ``0``\n:gem: **Total Bet Amount:** ``0``",
                            "inline" : True
                        },
                        {
                            "name" : "Participants",
                            "value" : "``Noone Has Joined Yet!``",
                            "inline" : True
                        }
                    ],
                    "footer" : {
                        "text" : "Crash"
                    },
                    "timestamp" : "2023-05-13T23:00:00.000Z"
                }
            ]
        }
        r = requests.post(
            url=crashwebhook,
            json=message,
            params={"wait": True})
        crash['MessageID'] = r.json()['id']
        time.sleep(15)
        totalwinnings = 0
        winnings = ""
        for user in crash['Users']:
            totalwinnings += round(user[1] * multi)
            add_gems(user[0], round(user[1] * multi))
            winnings += f"**{user[2]}:** ``{add_suffix(round(user[1] * multi))}``\n"
        gems = totalwinnings
        if gems >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
            gems_formatted = f"{gems / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
        elif gems >= 1000000000 :  # if gems are greater than or equal to 1 billion
            gems_formatted = f"{gems / 1000000000:.1f}b"  # display gems in billions with one decimal point
        elif gems >= 1000000 :  # if gems are greater than or equal to 1 million
            gems_formatted = f"{gems / 1000000:.1f}m"  # display gems in millions with one decimal point
        elif gems >= 1000 :  # if gems are greater than or equal to 1 thousand
            gems_formatted = f"{gems / 1000:.1f}k"  # display gems in thousands with one decimal point
        else :  # if gems are less than 1 thousand
            gems_formatted = str(gems)  # display gems as is
        print(multi)
        if multi >= 1.0:
            print("over")
            message = {
                "content" : f"",
                "embeds" : [
                    {
                        "title" : f":rocket: Crashed At x{multi}!",
                        "description" : "The Rocket Has Crashed!",
                        "color" : 10092393,
                        "fields" : [
                            {
                                "name" : "Details",
                                "value" : f":rocket: **Crashed:** <t:{crash['FinishTime']}:R>\n:exclamation: **Participants:** ``{len(crash['Users'])}``\n:gem: **Total Winnings:** ``{gems_formatted}``",
                                "inline" : True
                            },
                            {
                                "name" : "Winnings",
                                "value" : winnings,
                                "inline" : True
                            }
                        ],
                        "footer" : {
                            "text" : "Crash"
                        }
                    }
                ]
            }
            r = requests.patch(
                url=crashwebhook + f"/messages/{crash['MessageID']}",
                json=message)
            print(r.status_code)
        else:
            print("under")
            message = {
                "content" : f"",
                "embeds" : [
                    {
                        "title" : f":rocket: Crashed At x{multi}!",
                        "description" : "The Rocket Has Crashed!",
                        "color" : 16737637,
                        "fields" : [
                            {
                                "name" : "Details",
                                "value" : f":rocket: **Crashed:** <t:{crash['FinishTime']}:R>\n:exclamation: **Participants:** ``{len(crash['Users'])}``\n:gem: **Total Winnings:** ``{totalwinnings}``",
                                "inline" : True
                            },
                            {
                                "name" : "Winnings",
                                "value" : winnings,
                                "inline" : True
                            }
                        ],
                        "footer" : {
                            "text" : "Crash"
                        }
                    }
                ]
            }
            print(crash['MessageID'])
            r = requests.patch(
                url=crashwebhook + f"/messages/{crash['MessageID']}",
                json=message)
            print(r.status_code)
cr = threading.Thread(target=update_crash_game)
cr.start()
@bot.event
async def on_ready():
  print("Bot Is Online And Listening For Commands.")
  synced = await bot.tree.sync()
  print(f"Synced {len(synced)} command(s)")

@bot.tree.command(name="register", description="Register To Start Gambling!")
async def register(interaction: discord.Interaction):
    if not is_registered(str(interaction.user.id)):
        register_user(str(interaction.user.id))
        embed = discord.Embed(title=":white_check_mark: Registered User",
                              description=":gem: You Can Now Deposit, Withdraw And Gamble Your Gems! Have Fun!",
                              color=0x00ff33)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/register")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title=":x: Error",
                              description="You Are Already Registered!",
                              color=0xff0000)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/register")
        await interaction.response.send_message(embed=embed)
@bot.tree.command(name="deposit", description="Deposit Some Gems To Gamble")
async def deposit(interaction: discord.Interaction):
    if is_registered(str(interaction.user.id)):
        random_words = random.sample(words, 3)

        code = " ".join(random_words)

        codes.append([str(interaction.user.id), code])
        embed = discord.Embed(title=":gem: Deposit",
                              description=f":mailbox: Mail The Code: '{code}' To '{username}' With The Amount Of Gems You Want To Deposit. It Should Take Around 60s To Receive The Gems In Your Balance Once You Mail",
                              color=0x2eb9ff)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/deposit")
        await interaction.response.send_message(embed=embed)

    else:
        embed = discord.Embed(title=":x: Error",
                              description="You Are Not Registered!",
                              color=0xff0000)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/deposit")
        await interaction.response.send_message(embed=embed)
@bot.tree.command(name="balance", description="View Your Gem Balance")
async def balance(interaction: discord.Interaction):
    if is_registered(str(interaction.user.id)) :
        gems = get_gems(str(interaction.user.id))
        if gems >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
            gems_formatted = f"{gems / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
        elif gems >= 1000000000 :  # if gems are greater than or equal to 1 billion
            gems_formatted = f"{gems / 1000000000:.1f}b"  # display gems in billions with one decimal point
        elif gems >= 1000000 :  # if gems are greater than or equal to 1 million
            gems_formatted = f"{gems / 1000000:.1f}m"  # display gems in millions with one decimal point
        elif gems >= 1000 :  # if gems are greater than or equal to 1 thousand
            gems_formatted = f"{gems / 1000:.1f}k"  # display gems in thousands with one decimal point
        else :  # if gems are less than 1 thousand
            gems_formatted = str(gems)  # display gems as is

        embed = discord.Embed(title=":gem: Balance",
                              description=f"You Currently Have {gems_formatted} Gems!",
                              color=0x2eb9ff)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/balance")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title=":x: Error",
                              description="You Are Not Registered!",
                              color=0xff0000)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/balance")
        await interaction.response.send_message(embed=embed)
@bot.tree.command(name="withdraw", description="Withdraw Gems")
@app_commands.describe(amount="The Amount Of Gems To Withdraw")
@app_commands.describe(uname="The Username To Send The Gems To")
async def withdraw(interaction: discord.Interaction, amount: str, uname: str):
    amount = suffix_to_int(amount)
    if is_registered(str(interaction.user.id)) :
        if get_gems(str(interaction.user.id)) >= amount:
            subtract_gems(str(interaction.user.id), amount)
            gems = amount
            if gems >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
                gems_formatted = f"{gems / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
            elif gems >= 1000000000 :  # if gems are greater than or equal to 1 billion
                gems_formatted = f"{gems / 1000000000:.1f}b"  # display gems in billions with one decimal point
            elif gems >= 1000000 :  # if gems are greater than or equal to 1 million
                gems_formatted = f"{gems / 1000000:.1f}m"  # display gems in millions with one decimal point
            elif gems >= 1000 :  # if gems are greater than or equal to 1 thousand
                gems_formatted = f"{gems / 1000:.1f}k"  # display gems in thousands with one decimal point
            else :  # if gems are less than 1 thousand
                gems_formatted = str(gems)  # display gems as is
            message = {
                "content" : f"<@{interaction.user.id}> Withdrew {gems_formatted}!"
            }
            requests.post(
                url=withwebhook,
                json=message)
            send_message(f"{uname},{amount}")
            embed = discord.Embed(title=":gem: Withdraw",
                                  description=f"Withdrew {gems_formatted} Gems. It Should Take Around 60s To Recieve The Gems In The Mail On Your Account: {uname}",
                                  color=0x2eb9ff)
            embed.set_author(name="Gamble Bot",
                             icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
            embed.set_footer(text="/withdraw")
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title=":x: Error",
                                  description="You Are Too Poor For This Withdraw xD!",
                                  color=0xff0000)
            embed.set_author(name="Gamble Bot",
                             icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
            embed.set_footer(text="/withdraw")
            await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title=":x: Error",
                              description="You Are Not Registered!",
                              color=0xff0000)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/withdraw")
        await interaction.response.send_message(embed=embed)
@bot.tree.command(name="tip", description="Send Someone Gems")
@app_commands.describe(user="The User To Send To")
@app_commands.describe(amount="Amount To Send")
async def tip(interaction: discord.Interaction, amount: str, user: discord.Member):
    amount = suffix_to_int(amount)
    if is_registered(str(interaction.user.id)) :
        if is_registered(str(user.id)):
            if get_gems(str(interaction.user.id)) >= amount :
                subtract_gems(str(interaction.user.id), amount)
                time.sleep(0.5)
                add_gems(str(user.id), amount)
                gems = amount
                if gems >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
                    gems_formatted = f"{gems / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
                elif gems >= 1000000000 :  # if gems are greater than or equal to 1 billion
                    gems_formatted = f"{gems / 1000000000:.1f}b"  # display gems in billions with one decimal point
                elif gems >= 1000000 :  # if gems are greater than or equal to 1 million
                    gems_formatted = f"{gems / 1000000:.1f}m"  # display gems in millions with one decimal point
                elif gems >= 1000 :  # if gems are greater than or equal to 1 thousand
                    gems_formatted = f"{gems / 1000:.1f}k"  # display gems in thousands with one decimal point
                else :  # if gems are less than 1 thousand
                    gems_formatted = str(gems)  # display gems as is
                embed = discord.Embed(title=":gem: Send Gems",
                                      description=f"Sent {gems_formatted} Gems To {user.display_name}!",
                                      color=0x2eb9ff)
                embed.set_author(name="Gamble Bot",
                                 icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                embed.set_footer(text="/tip")
                await interaction.response.send_message(embed=embed)
            else :
                embed = discord.Embed(title=":x: Error",
                                      description="You Are Too Poor For This Tip XD!",
                                      color=0xff0000)
                embed.set_author(name="Gamble Bot",
                                 icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                embed.set_footer(text="/tip")
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title=":x: Error",
                                  description="The User You Are Trying To Send Gems To Isn't Registered!",
                                  color=0xff0000)
            embed.set_author(name="Gamble Bot",
                             icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
            embed.set_footer(text="/tip")
            await interaction.response.send_message(embed=embed)
    else :
        embed = discord.Embed(title=":x: Error",
                              description="You Are Not Registered!",
                              color=0xff0000)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/tip")
        await interaction.response.send_message(embed=embed)
@bot.tree.command(name="coinflip", description="Coinflip")
async def coinflip(interaction: discord.Interaction, bet: str, side: CoinSide):
    bet = suffix_to_int(bet)
    if is_registered(str(interaction.user.id)):
        if bet >= 1000000:
            if get_gems(str(interaction.user.id)) >= bet:
                randintgen = random.randint(0, 100)
                if randintgen <= 35:
                    choice = side.value
                else:
                    if side.value == "Heads":
                        choice = "Tails"
                    else:
                        choice = "Heads"
                if choice == side.value:
                    add_gems(str(interaction.user.id), round(bet/1.1))
                    gems = bet
                    if gems >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
                        gems_formatted = f"{gems / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
                    elif gems >= 1000000000 :  # if gems are greater than or equal to 1 billion
                        gems_formatted = f"{gems / 1000000000:.1f}b"  # display gems in billions with one decimal point
                    elif gems >= 1000000 :  # if gems are greater than or equal to 1 million
                        gems_formatted = f"{gems / 1000000:.1f}m"  # display gems in millions with one decimal point
                    elif gems >= 1000 :  # if gems are greater than or equal to 1 thousand
                        gems_formatted = f"{gems / 1000:.1f}k"  # display gems in thousands with one decimal point
                    else :  # if gems are less than 1 thousand
                        gems_formatted = str(gems)  # display gems as is
                    embed = discord.Embed(title=":white_check_mark: You Won!",
                                          description=f"You Flipped A Coin! It Landed On {choice}! You Won {gems_formatted}!",
                                          color=0x00ff33)
                    embed.set_author(name="Gamble Bot",
                                     icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                    embed.set_footer(text="/tip")
                    await interaction.response.send_message(embed=embed)
                else:
                    subtract_gems(str(interaction.user.id), int(bet))
                    gems = bet
                    if gems >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
                        gems_formatted = f"{gems / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
                    elif gems >= 1000000000 :  # if gems are greater than or equal to 1 billion
                        gems_formatted = f"{gems / 1000000000:.1f}b"  # display gems in billions with one decimal point
                    elif gems >= 1000000 :  # if gems are greater than or equal to 1 million
                        gems_formatted = f"{gems / 1000000:.1f}m"  # display gems in millions with one decimal point
                    elif gems >= 1000 :  # if gems are greater than or equal to 1 thousand
                        gems_formatted = f"{gems / 1000:.1f}k"  # display gems in thousands with one decimal point
                    else :  # if gems are less than 1 thousand
                        gems_formatted = str(gems)  # display gems as is
                    embed = discord.Embed(title=":x: You Lost",
                                          description=f"You Flipped A Coin! It Landed On {choice}! You Lost {gems_formatted}!",
                                          color=0xff0000)
                    embed.set_author(name="Gamble Bot",
                                     icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                    embed.set_footer(text="/tip")
                    await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title=":x: Error",
                                      description="You Are Too Poor!",
                                      color=0xff0000)
                embed.set_author(name="Gamble Bot",
                                 icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                embed.set_footer(text="/coinflip")
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title=":x: Error",
                                  description="You Cannot Bet Under 1m!",
                                  color=0xff0000)
            embed.set_author(name="Gamble Bot",
                             icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
            embed.set_footer(text="/coinflip")
            await interaction.response.send_message(embed=embed)
    else :
        embed = discord.Embed(title=":x: Error",
                              description="You Are Not Registered!",
                              color=0xff0000)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/coinflip")
        await interaction.response.send_message(embed=embed)
@bot.tree.command(name="create-rps-game", description="Start A Game Of Rock Paper Scissors (PVP)")
async def createrps(interaction: discord.Interaction, bet: str, side: RPSSide):
    bet = suffix_to_int(bet)
    if is_registered(str(interaction.user.id)) :
        if get_gems(str(interaction.user.id)) >= bet:
            letters = string.ascii_letters
            random_letters = random.sample(letters, 10)
            game_code = ''.join(random_letters)
            rpsgames.append([str(interaction.user.id), side.value, bet, game_code])
            gems = bet
            if gems >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
                gems_formatted = f"{gems / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
            elif gems >= 1000000000 :  # if gems are greater than or equal to 1 billion
                gems_formatted = f"{gems / 1000000000:.1f}b"  # display gems in billions with one decimal point
            elif gems >= 1000000 :  # if gems are greater than or equal to 1 million
                gems_formatted = f"{gems / 1000000:.1f}m"  # display gems in millions with one decimal point
            elif gems >= 1000 :  # if gems are greater than or equal to 1 thousand
                gems_formatted = f"{gems / 1000:.1f}k"  # display gems in thousands with one decimal point
            else :  # if gems are less than 1 thousand
                gems_formatted = str(gems)  # display gems as is
            embed = discord.Embed(title=":gem: Created Game",
                                  description=f"Created Game Of Rock Paper Scissors, Waiting For Someone To Join",
                                  color=0x2eb9ff)
            embed.set_author(name="Gamble Bot",
                             icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
            embed.add_field(name="Commands", value=f":white_check_mark: **Join Game:** ``/join-rps-game``\n:x: **Close Game:** ``/close-rps-game``", inline=True)
            embed.add_field(name="Details",value=f"\n:keyboard: **Game Id:** ``{game_code}``\n:gem: **Bet:** ``{gems_formatted}``",inline=True)
            embed.set_footer(text=f"Game ID: {game_code}")
            await interaction.response.send_message(embed=embed)
    else :
        embed = discord.Embed(title=":x: Error",
                              description="You Are Not Registered!",
                              color=0xff0000)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/rps")
        await interaction.response.send_message(embed=embed)
@bot.tree.command(name="close-rps-game", description="Close An RPS Game")
async def closerps(interaction: discord.Interaction, game_id: str):
    if is_registered(str(interaction.user.id)) :
        found = False
        for game in rpsgames:
            if game_id == game[3]:
                found = True
        if found == False:
            embed = discord.Embed(title=":x: Error",
                                  description="Game Does Not Exist!",
                                  color=0xff0000)
            embed.set_author(name="Gamble Bot",
                             icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
            embed.set_footer(text="/rps")
            await interaction.response.send_message(embed=embed)
        else:
            isowner = False
            for game in rpsgames :
                if game_id == game[3] and str(interaction.user.id) == game[0]:
                    isowner = True
            if not isowner:
                embed = discord.Embed(title=":x: Error",
                                      description="You Are Not The Owner Of This Game!",
                                      color=0xff0000)
                embed.set_author(name="Gamble Bot",
                                 icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                embed.set_footer(text="/rps")
                await interaction.response.send_message(embed=embed)
            else:
                for game in rpsgames :
                    if game_id == game[3]:
                        rpsgames.remove(game)
                embed = discord.Embed(title=":white_check_mark: Closed Game!",
                                      description=f"Game With Id: ``{game_id}`` Has Been Closed",
                                      color=0x00ff33)
                embed.set_author(name="Gamble Bot",
                                 icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                embed.set_footer(text="/tip")
                await interaction.response.send_message(embed=embed)
    else :
        embed = discord.Embed(title=":x: Error",
                              description="You Are Not Registered!",
                              color=0xff0000)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/rps")
        await interaction.response.send_message(embed=embed)
@bot.tree.command(name="join-rps-game", description="Join A Game Of Rock Paper Scissors (PVP)")
async def joinrps(interaction: discord.Interaction, game_id: str, side: RPSSide):
    if is_registered(str(interaction.user.id)) :
        found = False
        for game in rpsgames :
            if game_id == game[3] :
                found = True
        if found == False :
            embed = discord.Embed(title=":x: Error",
                                  description="Game Does Not Exist!",
                                  color=0xff0000)
            embed.set_author(name="Gamble Bot",
                             icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
            embed.set_footer(text="/rps")
            await interaction.response.send_message(embed=embed)
        else:
            game_data = []
            for game in rpsgames :
                if game_id == game[3] :
                    game_data = game
            if game_data[0] == str(interaction.user.id):
                embed = discord.Embed(title=":x: Error",
                                      description="You Are The Owner Of This Game (Bot RPS Comming Soon)!",
                                      color=0xff0000)
                embed.set_author(name="Gamble Bot",
                                 icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                embed.set_footer(text="/rps")
                await interaction.response.send_message(embed=embed)
            else:
                if get_gems(str(interaction.user.id)) >= game_data[2]:
                    for game in rpsgames :
                        if game_id == game[3] :
                            rpsgames.remove(game)
                    winner = ""
                    owner_side = game_data[1]
                    competitor_side = side.value

                    if owner_side == competitor_side :
                        # It's a tie
                        winner = "Tie"
                    elif owner_side == "Rock" and competitor_side == "Scissors" :
                        # Owner wins with rock
                        winner = "Owner"
                    elif owner_side == "Paper" and competitor_side == "Rock" :
                        # Owner wins with paper
                        winner = "Owner"
                    elif owner_side == "Scissors" and competitor_side == "Paper" :
                        # Owner wins with scissors
                        winner = "Owner"
                    else :
                        # Competitor wins
                        winner = "Competitor"
                    gems = game_data[2]
                    if gems >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
                        gems_formatted = f"{gems / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
                    elif gems >= 1000000000 :  # if gems are greater than or equal to 1 billion
                        gems_formatted = f"{gems / 1000000000:.1f}b"  # display gems in billions with one decimal point
                    elif gems >= 1000000 :  # if gems are greater than or equal to 1 million
                        gems_formatted = f"{gems / 1000000:.1f}m"  # display gems in millions with one decimal point
                    elif gems >= 1000 :  # if gems are greater than or equal to 1 thousand
                        gems_formatted = f"{gems / 1000:.1f}k"  # display gems in thousands with one decimal point
                    else :  # if gems are less than 1 thousand
                        gems_formatted = str(gems)  # display gems as is
                    if winner == "Tie":
                        embed = discord.Embed(title=":yellow_square: Nobody Won",
                                              description="Its A Draw!",
                                              color=0xffdf0f)
                        embed.set_author(name="Gamble Bot",
                                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                        embed.add_field(name="Sides", value=f"**Owner:** ``{owner_side}``\n**Competitor:** ``{competitor_side}``")
                        embed.set_footer(text="/rps")
                        await interaction.response.send_message(embed=embed,content=f"<@{interaction.user.id}> <@{game_data[0]}>")
                    if winner == "Competitor":
                        subtract_gems(str(game_data[0]), int(game_data[2]))
                        add_gems(str(interaction.user.id), round(game_data[2]/1.1))
                        embed = discord.Embed(title=":white_check_mark: Competitor Won!",
                                              description=f"You Won The Game! {gems_formatted} Gems Have Been Added To Your Account And Taken From The Game Owners Account!",
                                              color=0x00ff33)
                        embed.set_author(name="Gamble Bot",
                                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                        embed.add_field(name="Sides",
                                        value=f"**Owner:** ``{owner_side}``\n**Competitor:** ``{competitor_side}``")
                        embed.set_footer(text="/rps")
                        await interaction.response.send_message(embed=embed,content=f"<@{interaction.user.id}> <@{game_data[0]}>")
                    if winner == "Owner":
                        add_gems(str(game_data[0]), round(game_data[2]/1.1))
                        subtract_gems(str(interaction.user.id), int(game_data[2]))
                        embed = discord.Embed(title=":x: Competitor Lost!",
                                              description=f"You Lost The Game! {gems_formatted} Gems Will Be Taken From Your Account And Added To The Game Owner's Account!",
                                              color=0xff0000)
                        embed.set_author(name="Gamble Bot",
                                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                        embed.add_field(name="Sides",
                                        value=f"**Owner:** ``{owner_side}``\n**Competitor:** ``{competitor_side}``")
                        embed.set_footer(text="/rps")
                        await interaction.response.send_message(embed=embed,content=f"<@{interaction.user.id}> <@{game_data[0]}>")
                else:
                    embed = discord.Embed(title=":x: Error",
                                          description="You Are Too Poor To Join This Game!",
                                          color=0xff0000)
                    embed.set_author(name="Gamble Bot",
                                     icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                    embed.set_footer(text="/rps")
                    await interaction.response.send_message(embed=embed)
    else :
        embed = discord.Embed(title=":x: Error",
                              description="You Are Not Registered!",
                              color=0xff0000)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/rps")
        await interaction.response.send_message(embed=embed)
@bot.tree.command(name="create-rain", description="Join A Game Of Rock Paper Scissors (PVP)")
async def createrain(interaction: discord.Interaction, amount: str, duration: int):
    amount = suffix_to_int(amount)
    if is_registered(str(interaction.user.id)) :
        if interaction.user.id != 0:
            if get_gems(str(interaction.user.id)) >= amount:
                subtract_gems(str(interaction.user.id), amount)
                embed = discord.Embed(title=":white_check_mark: Created Rain!",
                                      description=f"Details Will Be Posted In #gem-rains!",
                                      color=0x00ff33)
                embed.set_author(name="Gamble Bot",
                                 icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                embed.set_footer(text="/create-rain")
                await interaction.response.send_message(embed=embed)

                def thing():
                    gems = amount
                    if gems >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
                        gems_formatted = f"{gems / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
                    elif gems >= 1000000000 :  # if gems are greater than or equal to 1 billion
                        gems_formatted = f"{gems / 1000000000:.1f}b"  # display gems in billions with one decimal point
                    elif gems >= 1000000 :  # if gems are greater than or equal to 1 million
                        gems_formatted = f"{gems / 1000000:.1f}m"  # display gems in millions with one decimal point
                    elif gems >= 1000 :  # if gems are greater than or equal to 1 thousand
                        gems_formatted = f"{gems / 1000:.1f}k"  # display gems in thousands with one decimal point
                    else :  # if gems are less than 1 thousand
                        gems_formatted = str(gems)  # display gems as is
                    message = {
                        "content" : f"",
                        "embeds": [
                            {
                                "title" : ":gem: New Rain!",
                                "description" : f"A Rain Has Been Started By <@{interaction.user.id}>!",
                                "color" : 5814783,
                                "fields" : [
                                    {
                                        "name" : "Details",
                                        "value" : f":gem: **Amount:** ``{gems_formatted}``\n:clock1: **Ends:** <t:{round(time.time()) + duration}:R>\n:exclamation: **Entries:** ``0``\n:coin: **Gems Per Person:** ``0``",
                                        "inline" : True
                                    }
                                ]
                            }
                        ]
                    }
                    r = requests.post(
                        url=rainwebhook,
                        json=message,
                        params={"wait": True})
                    rains.append([amount, round(time.time()) + duration, [], r.json()['id'], round(time.time()) + duration])
                    rain = rains[-1]
                    time.sleep(duration)
                    gems_each = rain[0] / len(rain[2])
                    gems_each = round(gems_each)
                    for person in rain[2]:
                        add_gems(person, gems_each)
                thread = threading.Thread(target=thing)
                thread.start()
            else:
                embed = discord.Embed(title=":x: Error",
                                      description="You Dont Have Enough Gems To Make This Rain.",
                                      color=0xff0000)
                embed.set_author(name="Gamble Bot",
                                 icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                embed.set_footer(text="/create-rain")
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title=":x: Error",
                                  description="Only InSpirX And Henrymistert Can Do This.",
                                  color=0xff0000)
            embed.set_author(name="Gamble Bot",
                             icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
            embed.set_footer(text="/create-rain")
            await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title=":x: Error",
                              description="You Are Not Registered!",
                              color=0xff0000)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/create-rain")
        await interaction.response.send_message(embed=embed)
@bot.tree.command(name="join-all-rains", description="Join A Game Of Rock Paper Scissors (PVP)")
async def joinrain(interaction: discord.Interaction):
    if is_registered(str(interaction.user.id)) :
        joined = 0
        for rain in rains:
            if str(interaction.user.id) not in rain[2]:
                rain[2].append(str(interaction.user.id))
                gems = round(rain[0]/len(rain[2]))
                if gems >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
                    gems_formatted = f"{gems / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
                elif gems >= 1000000000 :  # if gems are greater than or equal to 1 billion
                    gems_formatted = f"{gems / 1000000000:.1f}b"  # display gems in billions with one decimal point
                elif gems >= 1000000 :  # if gems are greater than or equal to 1 million
                    gems_formatted = f"{gems / 1000000:.1f}m"  # display gems in millions with one decimal point
                elif gems >= 1000 :  # if gems are greater than or equal to 1 thousand
                    gems_formatted = f"{gems / 1000:.1f}k"  # display gems in thousands with one decimal point
                else :  # if gems are less than 1 thousand
                    gems_formatted = str(gems)  # display gems as is
                gems2 = rain[0]
                if gems2 >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
                    gems_formatted2 = f"{gems2 / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
                elif gems2 >= 1000000000 :  # if gems are greater than or equal to 1 billion
                    gems_formatted2 = f"{gems2 / 1000000000:.1f}b"  # display gems in billions with one decimal point
                elif gems2 >= 1000000 :  # if gems are greater than or equal to 1 million
                    gems_formatted2 = f"{gems2 / 1000000:.1f}m"  # display gems in millions with one decimal point
                elif gems2 >= 1000 :  # if gems are greater than or equal to 1 thousand
                    gems_formatted2 = f"{gems2 / 1000:.1f}k"  # display gems in thousands with one decimal point
                else :  # if gems are less than 1 thousand
                    gems_formatted2 = str(gems2)  # display gems as is
                message = {
                    "content" : f"",
                    "embeds" : [
                        {
                            "title" : ":gem: New Rain!",
                            "description" : f"A Rain Has Been Started By <@{interaction.user.id}>!",
                            "color" : 5814783,
                            "fields" : [
                                {
                                    "name" : "Details",
                                    "value" : f":gem: **Amount:** ``{gems_formatted2}``\n:clock1: **Ends:** <t:{rain[4]}:R>\n:exclamation: **Entries:** ``{len(rain[2])}``\n:coin: **Gems Per Person:** ``{gems_formatted}``",
                                    "inline" : True
                                }
                            ]
                        }
                    ]
                }
                r = requests.patch(
                    url=rainwebhook + f"/messages/{rain[3]}",
                    json=message)
                joined = joined + 1
        embed = discord.Embed(title=":white_check_mark: Joined Rains!",
                              description=f"Joined {joined} Rains!",
                              color=0x00ff33)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="rains")
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title=":x: Error",
                              description="You Are Not Registered!",
                              color=0xff0000)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/join-all-rains")
        await interaction.response.send_message(embed=embed)
def get_win_chance(multiplier):
    win_chance = 50 * (1.5 / multiplier) * 1.1  # Reduce win chance by 5%
    return win_chance
@bot.tree.command(name="upgrader", description="Bet A Certain Amount Of Gems On A Multiplier And Have A Chance To Win")
async def upgrader(interaction: discord.Interaction, bet: str, multiplier: float):
    if multiplier >= 1.5 and multiplier <= 5:
        bet2 = bet
        bet = suffix_to_int(bet)
        if is_registered(str(interaction.user.id)):
            if bet >= 1000000:
                if get_gems(str(interaction.user.id)) >= bet:
                    win_chance = get_win_chance(multiplier)
                    outcome = random.uniform(0, 100)
                    winnings = round((bet*multiplier)/1.1)
                    subtract_gems(str(interaction.user.id), bet)
                    if outcome <= win_chance :
                        add_gems(str(interaction.user.id), winnings)
                        gems = winnings
                        if gems >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
                            gems_formatted = f"{gems / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
                        elif gems >= 1000000000 :  # if gems are greater than or equal to 1 billion
                            gems_formatted = f"{gems / 1000000000:.1f}b"  # display gems in billions with one decimal point
                        elif gems >= 1000000 :  # if gems are greater than or equal to 1 million
                            gems_formatted = f"{gems / 1000000:.1f}m"  # display gems in millions with one decimal point
                        elif gems >= 1000 :  # if gems are greater than or equal to 1 thousand
                            gems_formatted = f"{gems / 1000:.1f}k"  # display gems in thousands with one decimal point
                        else :  # if gems are less than 1 thousand
                            gems_formatted = str(gems)  # display gems as is
                        embed = discord.Embed(title=":white_check_mark: You Won!",
                                              description=f"You Won The Upgrade!",
                                              color=0x00ff33)
                        embed.set_author(name="Gamble Bot",
                                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                        embed.add_field(name="Details", value=f":gem: **Bet:** ``{bet2}``\n:gem: **Winnings:** ``{gems_formatted}``\n:four_leaf_clover: **Win Chance:** ``{win_chance}%``\n:star2: **Target Multiplier:** ``{multiplier}``")
                        embed.set_footer(text="upgrader")
                        await interaction.response.send_message(embed=embed)
                    else:
                        gems = winnings
                        if gems >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
                            gems_formatted = f"{gems / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
                        elif gems >= 1000000000 :  # if gems are greater than or equal to 1 billion
                            gems_formatted = f"{gems / 1000000000:.1f}b"  # display gems in billions with one decimal point
                        elif gems >= 1000000 :  # if gems are greater than or equal to 1 million
                            gems_formatted = f"{gems / 1000000:.1f}m"  # display gems in millions with one decimal point
                        elif gems >= 1000 :  # if gems are greater than or equal to 1 thousand
                            gems_formatted = f"{gems / 1000:.1f}k"  # display gems in thousands with one decimal point
                        else :  # if gems are less than 1 thousand
                            gems_formatted = str(gems)  # display gems as is
                        embed = discord.Embed(title=":x: You Lost!",
                                              description=f"You Lost The Upgrade!",
                                              color=0xff0000)
                        embed.set_author(name="Gamble Bot",
                                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                        embed.add_field(name="Details",
                                        value=f":gem: **Bet:** ``{bet2}``\n:gem: **Potential Winnings:** ``{gems_formatted}``\n:four_leaf_clover: **Win Chance:** ``{win_chance}%``\n:star2: **Target Multiplier:** ``{multiplier}``")
                        embed.set_footer(text="upgrader")
                        await interaction.response.send_message(embed=embed)
                else:
                    embed = discord.Embed(title=":x: Error",
                                          description="You Are Too Poor!",
                                          color=0xff0000)
                    embed.set_author(name="Gamble Bot",
                                     icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                    embed.set_footer(text="/coinflip")
                    await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title=":x: Error",
                                      description="You Cannot Bet Under 1m!",
                                      color=0xff0000)
                embed.set_author(name="Gamble Bot",
                                 icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                embed.set_footer(text="/coinflip")
                await interaction.response.send_message(embed=embed)
        else :
            embed = discord.Embed(title=":x: Error",
                                  description="You Are Not Registered!",
                                  color=0xff0000)
            embed.set_author(name="Gamble Bot",
                             icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
            embed.set_footer(text="/coinflip")
            await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title=":x: Error",
                              description="Min Multiplier Is 1.5 And The Max Is 5!",
                              color=0xff0000)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/coinflip")
        await interaction.response.send_message(embed=embed)
@bot.tree.command(name="join-crash", description="Join The Current Game Of Crash")
async def joincrash(interaction: discord.Interaction, bet: str):
    bet2 = bet
    bet = int(suffix_to_int(bet))
    if is_registered(str(interaction.user.id)) :
        if get_gems(str(interaction.user.id)) >= bet:
            subtract_gems(str(interaction.user.id), bet)
            totalwinnings = 0
            winnings = ""
            crash['Users'].append([str(interaction.user.id), bet, interaction.user.display_name])
            for user in crash['Users'] :
                totalwinnings += user[1]
                gems = user[1]
                if gems >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
                    gems_formatted = f"{gems / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
                elif gems >= 1000000000 :  # if gems are greater than or equal to 1 billion
                    gems_formatted = f"{gems / 1000000000:.1f}b"  # display gems in billions with one decimal point
                elif gems >= 1000000 :  # if gems are greater than or equal to 1 million
                    gems_formatted = f"{gems / 1000000:.1f}m"  # display gems in millions with one decimal point
                elif gems >= 1000 :  # if gems are greater than or equal to 1 thousand
                    gems_formatted = f"{gems / 1000:.1f}k"  # display gems in thousands with one decimal point
                else :  # if gems are less than 1 thousand
                    gems_formatted = str(gems)  # display gems as is
                winnings += f"**{user[2]}:** ``{gems_formatted}``\n"
            gems = totalwinnings
            if gems >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
                gems_formatted = f"{gems / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
            elif gems >= 1000000000 :  # if gems are greater than or equal to 1 billion
                gems_formatted = f"{gems / 1000000000:.1f}b"  # display gems in billions with one decimal point
            elif gems >= 1000000 :  # if gems are greater than or equal to 1 million
                gems_formatted = f"{gems / 1000000:.1f}m"  # display gems in millions with one decimal point
            elif gems >= 1000 :  # if gems are greater than or equal to 1 thousand
                gems_formatted = f"{gems / 1000:.1f}k"  # display gems in thousands with one decimal point
            else :  # if gems are less than 1 thousand
                gems_formatted = str(gems)  # display gems as is

            message = {
                "content" : f"",
                "embeds" : [
                    {
                        "title" : f":rocket: Crash",
                        "description" : "A New Game Of Crash Has Started! Type /join-crash With The Amount Of Gems To Bet To Join!",
                        "color" : 5814783,
                        "fields" : [
                            {
                                "name" : "Details",
                                "value" : f":rocket: **Crashes:** <t:{crash['FinishTime']}:R>\n:exclamation: **Participants:** ``{len(crash['Users'])}``\n:gem: **Total Bet Amount:** ``{gems_formatted}``",
                                "inline" : True
                            },
                            {
                                "name" : "Participants",
                                "value" : winnings,
                                "inline" : True
                            }
                        ],
                        "footer" : {
                            "text" : "Crash"
                        }
                    }
                ]
            }
            r = requests.patch(
                url=crashwebhook + f"/messages/{crash['MessageID']}",
                json=message)

            embed = discord.Embed(title=":white_check_mark: Joined Game",
                                  description=f"You Bet {bet2} On The Crash Round!",
                                  color=0x2eb9ff)
            embed.set_author(name="Gamble Bot",
                             icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
            embed.set_footer(text="/crash")
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title=":x: Error",
                                  description="You Are Too Poor!",
                                  color=0xff0000)
            embed.set_author(name="Gamble Bot",
                             icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
            embed.set_footer(text="/crash")
            await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title=":x: Error",
                              description="You Are Not Registered!",
                              color=0xff0000)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/crash")
        await interaction.response.send_message(embed=embed)
@bot.event
async def on_component_interaction(interaction):
    if interaction.component.custom_id == 'climb':
        await interaction.respond(content='Button was clicked!')

class ClimbButtons(discord.ui.View):
    def __init__(self, crashchance, multiplier, bet):
        super().__init__(timeout=None)
        self.crashchance = crashchance
        self.multiplier = multiplier
        self.bet = bet
        self.clicked = False
    @discord.ui.button(label="Cashout", custom_id="cashout", style=discord.ButtonStyle.green)
    async def Cashout(self, interaction: discord.Interaction, button: discord.Button):
        if not self.clicked:
            embed = discord.Embed(title=f":white_check_mark: Cashed Out At x{self.multiplier}!", description="Will You Climb Or Cashout?",
                                  color=0x00ff33)
            embed.set_author(name="Gamble Bot",
                             icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
            embed.set_footer(text="/climb")
            embed.add_field(name="Details",
                            value=f":gem: **Bet:** ``{add_suffix(self.bet)}``\n:gem: **Winnings:** ``{add_suffix(round(self.bet * self.multiplier))}``\n:star2: **Multiplier:** ``{self.multiplier}``")
            message = await interaction.response.send_message(embed=embed, content="")
            add_gems(str(interaction.user.id), round(self.bet * self.multiplier))
            self.clicked = True
    @discord.ui.button(label="Climb", custom_id="climb", style=discord.ButtonStyle.green)
    async def Climb(self, interaction: discord.Interaction, button: discord.Button):
        if not self.clicked:
            rand_numb = random.randint(0, 100)
            if rand_numb <= self.crashchance:
                embed = discord.Embed(title=f":x: Crashed At x{self.multiplier}!",
                                      description="You Fell!",
                                      color=0xff0000)
                embed.set_author(name="Gamble Bot",
                                 icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                embed.set_footer(text="/climb")
                embed.add_field(name="Details",
                                value=f":gem: **Bet:** ``{add_suffix(self.bet)}``\n:gem: **Potential Winnings:** ``{add_suffix(round(self.bet * self.multiplier))}``\n:star2: **Multiplier:** ``{self.multiplier}``\n:four_leaf_clover: **Fall Chance:** ``{self.crashchance}%``")
                await interaction.response.send_message(embed=embed)
            else:
                multiplier = round(self.multiplier + 0.1, 1)
                crashchance = self.crashchance + 5

                embed = discord.Embed(title=":white_check_mark: Success!", description="Will You Climb Or Cashout?",
                                      color=0x00ff33)
                embed.set_author(name="Gamble Bot",
                                 icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
                embed.set_footer(text="/climb")
                embed.add_field(name="Details",
                                value=f":gem: **Bet:** ``{add_suffix(self.bet)}``\n:gem: **Potential Winnings:** ``{add_suffix(round(self.bet * multiplier))}``\n:star2: **Multiplier:** ``{multiplier}``\n:four_leaf_clover: **Fall Chance:** ``{crashchance}%``")
                message = await interaction.response.send_message(embed=embed, content="",
                                                                  view=ClimbButtons(crashchance=crashchance,
                                                                                    multiplier=multiplier, bet=self.bet))
            self.clicked = True

@bot.tree.command(name="climb", description="Climb Up The Multipliers And Earn Big Gems!")
async def climb(interaction: discord.Interaction, bet: str):
    bet = suffix_to_int(bet)
    uid = str(interaction.user.id)
    if is_registered(str(interaction.user.id)):
        if get_gems(uid) >= bet:
            subtract_gems(uid, bet)
            multiplier = 1.0
            crashchance = 10

            embed = discord.Embed(title=":white_check_mark: Success!", description="Will You Climb Or Cashout?",color=0x00ff33)
            embed.set_author(name="Gamble Bot",
                                    icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
            embed.set_footer(text="/climb")
            embed.add_field(name="Details",value=f":gem: **Bet:** ``{add_suffix(bet)}``\n:gem: **Potential Winnings:** ``{add_suffix(round(bet*multiplier))}``\n:star2: **Multiplier:** ``{multiplier}``\n:four_leaf_clover: **Fall Chance:** ``{crashchance}%``")
            message = await interaction.response.send_message(embed=embed, content="", view=ClimbButtons(crashchance=crashchance,multiplier=multiplier,bet=bet))

        else:
            embed = discord.Embed(title=":x: Error",
                                  description="You Cannot Afford This Bet!",
                                  color=0xff0000)
            embed.set_author(name="Gamble Bot",
                             icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
            embed.set_footer(text="/climb")
            await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title=":x: Error",
                              description="You Are Not Registered!",
                              color=0xff0000)
        embed.set_author(name="Gamble Bot",
                         icon_url="https://cdn.itemsatis.com/uploads/post_images/pet-simulator-x-10b-gems-81004359.png")
        embed.set_footer(text="/climb")
        await interaction.response.send_message(embed=embed)


bot.run("MTEwMjk3MTA3NTA1NjM4NjA2OA.Gd7F9J.MpLrN7k10eMyLjBhjIIfDk5UYeqxetJgdOthRA")
print("ran")
