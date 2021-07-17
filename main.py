import os
from unicodedata import name
from bs4.builder import HTML
import discord
from dotenv import load_dotenv
from numpy.core.defchararray import array
from numpy.core.fromnumeric import var
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import numpy as np

load_dotenv()
#Bot Token
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
poolurl = "https://adapools.org/pool/f8cac661341d248b2194f93c257eefd1c9b122a6d82d449c3c559516"

pageepoch = requests.get("https://cardanocountdown.com")
soupepoch = BeautifulSoup(pageepoch.content, 'html.parser')
# daysleft2 = soupepoch.find(id="days").text


#Pool info from adapool.org
def poolinfo():
    pagepool = requests.get(poolurl)
    souppool = BeautifulSoup(pagepool.content, 'html.parser')
    poolarray = []
    for item in souppool.select(".text-muted span"):
        items = item.text.strip("\n")
        if items != "" and items not in poolarray:
            poolarray.append(items)
    poolarray.pop()

    # Pool info globals and variables
    global ticker
    global url
    global roa
    global livestake
    global activestake
    global pledge
    global lastreward
    global lifetimeblocks
    global luck
    global delegators

    ticker = poolarray[2]
    url = poolarray[3]
    roa = poolarray[4]
    livestake = poolarray[6]
    activestake = poolarray[7]
    pledge = poolarray[8]
    lastreward = poolarray[12].replace("minting ", "")
    lifetimeblocks = poolarray[16]
    luck = poolarray[17]
    delegators = poolarray[19]

#Current Epoch info
def epochinfo():
    pageepoch = requests.get("https://cardanocountdown.com")
    soupepoch = BeautifulSoup(pageepoch.content, 'html.parser')
    epocharray = []
    epochnamearray = []
    for x in soupepoch.select(".ul-row span"):
        countdown = x.text.strip("\n")
        if countdown != "" and countdown not in epocharray:
            epocharray.append(countdown)

    # Countdown globals and variables
    global daysleft
    global hoursleft
    global minutesleft
    global secondsleft
    global currentepoch

    daysleft = soupepoch.find(id="days").text
    hoursleft = soupepoch.find(id="hours").text
    minutesleft = soupepoch.find(id="minutes").text
    secondsleft = soupepoch.find(id="seconds").text
    currentepoch = soupepoch.find(class_="card-subtitle mb-2 text-muted").text
    currentepoch = re.sub('\D', '', currentepoch)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$pool'):
        poolinfo()
        epochinfo()
        embed=discord.Embed(
        title="Current Epoch: " + currentepoch,
        url="https://adapools.org/pool/f8cac661341d248b2194f93c257eefd1c9b122a6d82d449c3c559516",
        description="The Art of Happiness",
        color=discord.Color.blue())
        embed.set_author(name=ticker + " Staking Pool", url=url, icon_url="https://i.imgur.com/Qqz9Prl.png")
        embed.set_thumbnail(url="https://i.imgur.com/ZPvDa1Y.png")
        embed.add_field(name="**Live Stake**", value=livestake, inline=True)
        embed.add_field(name="**Lifetime Blocks**", value=lifetimeblocks, inline=True)
        embed.add_field(name="**Delegators**", value=delegators, inline=True)
        embed.add_field(name="**Pool Luck**", value=luck, inline=True)
        embed.add_field(name="**Last Reward**", value=lastreward, inline=True)
        embed.add_field(name="**ROA**", value=roa, inline=True)
        embed.set_footer(text="Next Epoch: " + daysleft + " days "+ hoursleft + " hours "+ minutesleft + " minutes "+ secondsleft + " seconds")
        await message.channel.send(embed = embed)

client.run(TOKEN)