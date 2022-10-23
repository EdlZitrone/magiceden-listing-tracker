import discord
import requests
import asyncio
from discord import Webhook
import aiohttp
import datetime

webhook_url = 'put your dicord webhook url here'
collections = ["magiceden", "collection", "symbols"]

specific_url = 'https://api-mainnet.magiceden.dev/v2/tokens/'
payload = {}
headers = {}


async def scan(collection):
    collection_url = f"https://api-mainnet.magiceden.dev/v2/collections/{collection}/activities?offset=0&limit=1"
    while True:
        response_old = requests.request("GET", collection_url, headers=headers, data=payload)
        await asyncio.sleep(3)
        response = requests.request("GET", collection_url, headers=headers, data=payload)
        if response.text != response_old.text:
            data = response.json()
            for doc in data:
                if doc["type"] == "list":
                    nft_response = requests.request("GET", specific_url+doc['tokenMint'], headers=headers, data=payload)
                    nft_data = nft_response.json()
                    embed = discord.Embed(
                        description=f"<a:PurpleStar:972624567833079889> Collection: {nft_data['collection']}\n"
                                    f"<a:YellowStar:972624567417860108> Name: {nft_data['name']}\n"
                                    f"<a:PurpleStar:972624567833079889> Type: {doc['type']}\n"
                                    f"<a:YellowStar:972624567417860108> Price: {doc['price']} SOL\n",
                        color=discord.Color.random(),
                        title=f"<a:BlueStar:972825132395556894> New Magiceden Listing!",
                        url=f"https://magiceden.io/item-details/{doc['tokenMint']}",
                        timestamp=datetime.datetime.utcnow())
                    embed.set_image(url=nft_data["image"])
                    embed.set_footer(text='\u200b Coded by EdlZitrone#6631', icon_url="https://i.imgur.com/uZIlRnK.png")
                    await send_webhook(embed)


async def send_webhook(embed):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, session=session)
        await webhook.send(embed=embed)


async def async_main():
    tasks = [
        asyncio.create_task(scan(entry))
        for entry in collections
    ]
    await asyncio.wait(tasks)

asyncio.run(async_main())
