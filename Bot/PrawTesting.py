# import praw
# import os
# from dotenv import load_dotenv
# from datetime import date
#
# load_dotenv()
#
# username = os.getenv("name")
# password = os.getenv("password")
#
# reddit = praw.Reddit(
#     client_id="PcvZi84yLqzsNA",
#     client_secret="CGfKgb3wKcOLNfW_X6uVwrgfTQc",
#     user_agent="PcvZi84yLqzsNA",
#     username=username,
#     password=password
# )
#
# # subreddits = reddit.user.subreddits()
# #
# # for sub in subreddits:
# #     print(sub)
# #
#
# user = reddit.user.me()
#
# # saved = user.saved(limit=1)
# #
# # for item in saved:
# #     print(item.subreddit)
# #     print(item.title)
# #     print(item.shortlink)
# #     print(item.created_utc)
# #     print(item.url)
# #     print()
#
#
# upvoted = user.upvoted(limit=5);
#
# for post in upvoted:
#     print(post.title)
#     print(date.fromtimestamp(post.created_utc))
#
# # @lack of a better way at the momment.
#
# # due to the fact that the save and upvoted functions don't have a time parameter for filtering
# # the posts I'll have to hash the name and timestamp of the last added post in discord and compare it
# # with the hash of every returned post from the generator.
# # As a start I could set the generator on a limit of 20 or so posts and make a request every 5-10 minutes
