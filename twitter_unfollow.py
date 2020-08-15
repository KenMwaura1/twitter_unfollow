
import tweepy
import pandas as pd
from datetime import datetime, timedelta
from environs import Env

env = Env()

# Reading the .env file
env.read_env()

API_KEY = env('API_KEY')
API_KEY_SECRET = env('API_KEY_SECRET')
ACCESS_TOKEN = env('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = env('ACCESS_TOKEN_SECRET')

USER = env('USER')

""" Any user you're following that hasn't posted during the DAYS_WITHOUT ACTIVITY
will be unfollowed """
DAYS_WITHOUT_ACTIVITY = 60

""" Any user that posts less than once in the last 5 days will be unfollowed """
DAILY_TWEET_FREQUENCY = 1. / 5

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

threshold = datetime.now() - timedelta(days=DAYS_WITHOUT_ACTIVITY)

count = 0
data = []

for user in api.friends_ids(USER):
    status = api.user_timeline(user, count=100)
    span = ((status[0].created_at - status[-1].created_at).days)
    frequency = (len(status) / span) if span > 0 else None
    if status[0].created_at < threshold or (frequency is not None and frequency < DAILY_TWEET_FREQUENCY):
        print(f"Unfollowing @{status[0].user.screen_name} ({status[0].user.name}). "
              f"Last status update on {status[0].created_at}. Frequency: {frequency:.2f} ")
        api.destroy_friendship(user)
        count += 1

print(f"You just unfollowed {count} accounts. @{USER} is now following {len(api.friends_ids(USER))}")
