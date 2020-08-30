'''
This program is for a Twitter bot that replies to mentions with a random fairy insult.
(Inspired by the TikTok trend)
Followed and modified a YouTube tutorial by CSDojo.

Creator: Inika Chikarmane
Date: 29th August, 2020
'''
import tweepy
import time
import random
import os

print('this is my twitter bot', flush=True)

# Gets the keys and secrets from set environment variables.
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = '/Users/Inika/Desktop/twitter-insult-bot/last_seen_id.txt'
FILE2_NAME = '/Users/Inika/Desktop/twitter-insult-bot/fairy_insults.txt'

# Returns the last seen Tweet ID from the file.


def retrieve_last_seen_id(file_name):

    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()

    return last_seen_id

# Stores the last seen Tweet ID in the file.


def store_last_seen_id(last_seen_id, file_name):

    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()

    return

# Loads the insults, and makes them into a list.


def insult_load(file_name):

    my_file = open(file_name, "r")
    content = my_file.read()
    content_list = content.split("\n")  # Separated by new line.
    my_file.close()

    return content_list

# Handles assessing mentions and then replying with a randomly chosen insult.


def reply_to_tweets(content):

    print('retrieving and replying to tweets...', flush=True)
    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    # Makes a list of mentions.
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')

    # Goes through the mentions, starting with the most recent.
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        print('found mention', flush=True)
        print('responding back...', flush=True)
        username = mention.user.screen_name
        reply = "@%s " % username + random.choice(content)
        api.update_status(status=reply, in_reply_to_status_id=mention.id)


while True:
    try:
        content = insult_load(FILE2_NAME)
        reply_to_tweets(content)
        time.sleep(25)

    # When it exceeds the # of requests allowed by Twitter, sleeps for 15 mins.
    except tweepy.TweepError:
        print("Rate Limit Error, wait 15 minutes...")
        time.sleep(60 * 15)

        continue

    except StopIteration:
        break
