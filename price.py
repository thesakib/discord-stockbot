# bot.py
import os
import requests
import json
import random
import discord
import re
from dotenv import load_dotenv
from discord.ext import commands

boy = "kazi"
randy = [
        f"Try it {boy}",
        f'Bingo! {boy}',
        (
            f'Cool. Cool cool {boy} cool cool {boy} cool, '
            f'no doubt no {boy} no doubt no {boy}.'
        ),
    ]

for x in range(5):
    response = random.choice(randy)
    print(response)
