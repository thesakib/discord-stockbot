# bot.py
import os
import requests
import json
import random
import discord
import re
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
# IEX_TOKEN = os.getenv('IEX_TOKEN')

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    for a in client.get_all_members():
        print(a)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    stock_re = re.search(r"\$[A-Z]{1,5}\b", message.content)

    if(stock_re != None):
        stock_name = stock_re.group()[1:]
        website = "https://finnhub.io/api/v1/quote?symbol=" + stock_name + "&token=c0c3a6f48v6o915a1bl0"
        r = requests.get(website)
        data = r.json()
        stock_price = data["c"]
        print(f"Last price for ${stock_name} is ${stock_price}")
        response = f"Last price for ${stock_name} is ${stock_price}"

        await message.channel.send(response)

    else:
        print("Found none")

client.run(TOKEN)
