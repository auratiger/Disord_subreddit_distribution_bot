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

# ==== util functions ====

def write_json(data, filename="data.json"):
    with open(filename, "w") as write_file:
        json.dump(data, write_file, indent=4)

async def delete_messages(channel):
    counter = 0
    async for message in channel.history(limit=200):
        print(message.content)
        await message.delete()

async def disable_reddit(channel):
    data["reddit_scrape_running"] = False
    await channel.send("scraping was disabled")

async def enable_reddit(channel):
    data["reddit_scrape_running"] = True
    await channel.send("scraping was anabled")

async def on_message_switch_handler(argument, channel):
    switcher = {
        "$del_messages": await delete_messages(channel),
        "$disable_reddit": await disable_reddit(channel),
        "$anable_reddit": await enable_reddit(channel)
    }
    switcher.get(argument, None)

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

    if(author == "Ani"):
        return
    else:
        on_message_switch_handler(msg, channel)

# === reddit api === #

async def manage_saved_posts(limit: int):
    last_saved = data["last_saved"]

    # fetch a dictionary of containing the saved posts, and the name of the last fetched post
    (saved, last_saved_post) = reddit_service.fetch_saved_posts(limit=limit, break_point=last_saved)

    # update the env variable "last_saved" with the latest saved_post
    data["last_saved"] = last_saved_post

    for key in saved:
        channel = None
        channel_id = data["channels"].get(key, None)

        if (channel_id == None):
            guild = client.get_guild(data["guild_id"])
            category_channel = discord.utils.get(guild.categories, name="Text Channels")

            channel = await category_channel.create_text_channel(key)

            data["channels"][key] = channel.id
        else:
            channel = client.get_channel(channel_id)

        post_list = saved[key]

        for i in range(len(post_list) - 1, -1, -1):
            post = post_list[i]
            await channel.send(post.shortlink)

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
        # print(post.url)
        print(post.shortlink)
        # print(post.permalink)

        await channel.send(post.shortlink)
        await asyncio.sleep(0.2)

initial_run = True

async def time_check():
    await client.wait_until_ready()

    if initial_run:
        limit = 500
    else:
        limit = data["limit"]

    while not client.is_closed() and data["reddit_scrape_running"]:

        # TODO need to add error handling !!

        await manage_saved_posts(limit)

        await manage_upvoted_posts(limit)

        # the timestamp of when the proccess has finished
        data["last_scrape_timestamp"] = time.time()

        await asyncio.sleep((60 * 6) + 5)

# === === === #

if __name__ == "__main__":
    try:
        client.loop.create_task(time_check())
        client.run(TOKEN)
    except Exception as e:
        print("Something went wrong: {0}".format((e)))
    finally:
        write_json(data)





