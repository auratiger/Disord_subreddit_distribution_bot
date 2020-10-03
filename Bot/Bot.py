import os
import asyncio
from datetime import datetime, timedelta
import time
import sched

import discord
from dotenv import load_dotenv

from RedditService import RedditService

# load env variables
load_dotenv()

# Discord Creds
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("guild"))

client = discord.Client()

# Reddit Creds
username = os.getenv("name")
password = os.getenv("password")
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
user_agent = os.getenv("user_agent")

reddit_service = RedditService(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)

reddit_running = True

# reddit_service.fetch_upvoted_links()
# reddit_service.fetch_saved_links()

# === events === #

@client.event
async def on_ready():
    print("Connected to Discord")

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

# Discord channel names are all lower case and the words are
# seperated by dashes (-) instead of spaces

async def time_check():
    await client.wait_until_ready()

    guild = client.get_guild(GUILD_ID)

    limit = int(os.getenv("limit"))

    while not client.is_closed() and reddit_running:

        last_saved = os.getenv("last_saved")

        (saved, last_saved_post) = reddit_service.fetch_saved_links(limit=limit, last_saved=last_saved)

        # update the env variable "last_saved" with the latest saved_post
        os.environ["last_saved"] = last_saved_post

        for key in saved:
            for post in saved[key]:
                channel = os.getenv(post.subreddit)

                if(channel == None):
                    pass






        await asyncio.sleep((60 * 5) + 5)

# === === === #


if __name__ == "__main__":
    client.run(TOKEN)
    # client.loop.create_task(time_check())




