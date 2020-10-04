import praw
from datetime import date

class RedditService(praw.Reddit):

    def __init__(self, client_id, client_secret, user_agent,
                 username, password, *args, **kwargs):
        super().__init__(client_id=client_id,
              client_secret=client_secret,
              user_agent=user_agent,
              username=username,
              password=password
              )

        self.user = self.user.me()


    def fetch_upvoted_posts(self, limit=10, break_point="") -> []:
        result = []
        last_post = ""
        upvoted = self.user.upvoted(limit=limit);

        counter = 0
        for post in upvoted:
            if(post.title == break_point):
                break
            elif(counter == 0):
                last_post = post.title
                counter += 1

            result.append(post)

        return (result, last_post)



    def fetch_saved_posts(self, limit, break_point):
        result = {}
        last_post = ""
        upvoted = self.user.saved(limit=limit);

        counter = 0
        for post in upvoted:
            if(post.title == break_point):
                break
            elif(counter == 0):
                last_post = post.title
                counter += 1

            subreddit = post.subreddit.display_name
            if(subreddit in result):
                result[subreddit].append(post)
            else:
                result[subreddit] = [post]

        return (result, last_post)


