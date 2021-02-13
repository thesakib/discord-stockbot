# bot.py
import os
import requests
import json
import random
import discord
import re
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


bot = commands.Bot(intents=intents, command_prefix='!')

def getStock(msg):
    stock_re = re.search(r"\$[A-Z]{1,5}\b", msg)
    if (stock_re != None):
        stock_name = stock_re.group()[1:]
        return stock_name
    else:
        return "None"


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    for a in bot.get_all_members():
        print(a)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    stock_name = getStock(message.content)
    if(stock_name != "None") and "!" not in message.content:
        website = "https://finnhub.io/api/v1/quote?symbol=" + stock_name + "&token=c0c3a6f48v6o915a1bl0"
        r = requests.get(website)
        data = r.json()
        stock_price = data["c"]
        print(f"Last price for ${stock_name} is ${stock_price}")
        response = f"Last price for ${stock_name} is ${stock_price}"

        await message.channel.send(response)

    else:
        print("Found none")
    await bot.process_commands(message)

@bot.command(name='full',brief='Detailed price command', description='Write \"!full\" followed by the symbol in upper-case for detailed price information.')
async def detailed_price(cntx, msg):
    if cntx.author == bot.user:
        return

    stock_name = getStock(msg)
    if(stock_name != "None"):
        print("connecting...")
        website = "https://finnhub.io/api/v1/quote?symbol=" + stock_name + "&token=c0c3a6f48v6o915a1bl0"
        r = requests.get(website)
        data = r.json()
        cur_price = data["c"]
        open_price = data["o"]
        close_price = data["pc"]
        high_price = data["h"]
        low_price = data["l"]

        response = f"```\nLatest update for ${stock_name}:\nCurrent Price : ${cur_price}\nOpen Price : ${open_price}\nPreviously Closed : ${close_price}\nToday's high : ${high_price}\nToday's Low : ${low_price}\n```"

        await cntx.send(response)
    else:
        return

@bot.command(name='analyst',brief='Analyst suggestion command',description='Write \"!analyst\" followed by the symbol in upper-case for the latest analyst suggestions.')
async def analyst(cntx, msg):
    if cntx.author == bot.user:
        return

    stock_name = getStock(msg)
    if(stock_name != "None"):
        print("connecting...")
        website = "https://finnhub.io/api/v1/stock/recommendation?symbol=" + stock_name + "&token=c0c3a6f48v6o915a1bl0"
        r = requests.get(website)
        data = r.json()
        strong_buy = data[0]["strongBuy"]
        buy = data[0]["buy"]
        hold = data[0]["hold"]
        sell = data[0]["sell"]
        strong_sell = data[0]["strongSell"]
        period = data[0]["period"]

        response = f"```\nAnalysts' update for ${stock_name} on {period}:\nStrong Buy : {strong_buy}\nBuy : {buy}\nHold : {hold}\nSell : {sell}\nStrong Sell : {strong_sell}\n```"

        await cntx.send(response)
    else:
        return

@bot.command(name='target',brief='Target prediction command', description ='\"!target\" followed by the symbol in upper-case for the 12 to 16 months price target prediction by the analyst')
async def target_price(cntx, msg):
    if cntx.author == bot.user:
        return

    stock_name = getStock(msg)
    if(stock_name != "None"):
        print("connecting...")
        website = "https://finnhub.io/api/v1/stock/price-target?symbol=" + stock_name + "&token=c0c3a6f48v6o915a1bl0"
        r = requests.get(website)
        data = r.json()
        targetHigh = data["targetHigh"]
        targetLow = data["targetLow"]
        targetMean = data["targetMean"]
        targetMedian = data["targetMedian"]
        lastUpdated = data["lastUpdated"]

        response = f"```\nAnalysts' 16-18 months target prediction for ${stock_name}  updated on {lastUpdated}:\nHigest Target : ${targetHigh}\nLowest Target : ${targetLow}\nMean Target : ${targetMean}\nMedian Target : ${targetMedian}```"

        await cntx.send(response)
    else:
        return

@bot.command(name='nick',brief='Change nickname', description='Write \"!nick\" followed by the name you want to use as your nickname.')
async def nickname(cntx, msg):
    if cntx.author == bot.user:
        return

        await msg.author.edit(nick = msg.content)
        response = f"{cntx.author.name} changed his nickname to {msg}"
        await cntx.send(response)



bot.run(TOKEN)
