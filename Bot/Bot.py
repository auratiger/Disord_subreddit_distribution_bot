import os
import asyncio
from datetime import datetime, timedelta
import time
import sched
import json

import discord
from dotenv import load_dotenv

from RedditService import RedditService

# load env variables
load_dotenv(override=True)

# load data
data = None
with open("data.json") as data_file:
    data = json.load(data_file)

# === Discord API ===
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client()

# === Reddit API ===
reddit_service = RedditService(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    user_agent=os.getenv("user_agent"),
    username=os.getenv("name"),
    password=os.getenv("password")
)

def write_json(data, filename="data.json"):
    with open(filename, "w") as write_file:
        json.dump(data, write_file, indent=4)

# === events === #

@client.event
async def on_ready():
    print("Connected to Discord")
    print(data)

@client.event
async def on_message(message):
    channel = message.channel
    author = message.author.name
    msg = message.content

    if(author.startswith("Ani")):
        return
    elif(msg.startswith("$del_messages")):
        counter = 0
        async for message in channel.history(limit=200):
            print(message.content)
            await message.delete()
        return
    elif(msg.startswith("$disable_reddit")):
        pass
    elif(msg.startswith("$anable_reddit")):
        pass

# === reddit api === #

async def manage_saved_posts(limit: int):
    last_saved = data["last_saved"]

    # fetch a dictionary of containing the saved posts, and the name of the last fetched post
    (saved, last_saved_post) = reddit_service.fetch_saved_posts(limit=limit, break_point=last_saved)

    # update the env variable "last_saved" with the latest saved_post
    data["last_saved"] = last_saved_post

    for key in saved:
        for post in saved[key]:
            channel = None
            subreddit_name = post.subreddit.display_name
            channel_id = os.getenv(subreddit_name)

            if (channel_id == None):
                guild = client.get_guild(data["guild_id"])
                category_channel = discord.utils.get(guild.categories, name="Text Channels")

                channel = await category_channel.create_text_channel(subreddit_name)

                os.environ[subreddit_name] = str(channel.id)
            else:
                channel = client.get_channel(channel_id)

            await channel.send("hello")

async def manage_upvoted_posts(limit: int):
    last_upvoted = data["last_upvoted"]

    # fetch a list of containing the upvoted posts, and the name of the last fetched post
    (upvoted, last_upvoted_post) = reddit_service.fetch_upvoted_posts(limit=limit, break_point=last_upvoted)

    # update the env variable "last_upvoted" with the latest saved_post
    data["last_upvoted"] = last_upvoted_post

    channel = None
    channel_id = data["channels"].get("upvotes", None)

    if (channel_id == None):
        guild = client.get_guild(data["guild_id"])
        category_channel = discord.utils.get(guild.categories, name="Text Channels")

        channel = await category_channel.create_text_channel("upvotes")

        data["channels"]["upvotes"] = channel.id
    else:
        channel = client.get_channel(channel_id)

    print(channel)
    for i in range(len(upvoted) - 1, -1, -1):
        post = upvoted[i]
        print(post.url)
        await channel.send(post.url)
        await asyncio.sleep(0.2)

async def time_check():
    await client.wait_until_ready()

    limit = data["limit"]

    while not client.is_closed() and data["reddit_scrape_running"]:

        # manage_saved_posts(limit)

        await manage_upvoted_posts(limit)

        write_json(data)

        await asyncio.sleep((60 * 5) + 5)

# === === === #

if __name__ == "__main__":
    client.loop.create_task(time_check())
    client.run(TOKEN)




