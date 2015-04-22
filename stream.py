from pync import Notifier
import time
import os
import json
import random
import urllib.request
import requests
from bs4 import BeautifulSoup
import tweepy
from keys import keys

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

class RetweetLDJAM(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        jsonData = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print('Tweet: ' + jsonData['user']['screen_name'], jsonData['text'].encode('ascii', 'ignore'))
        return True

    def on_error(self, status):
        print(status)

# START BOT
# ld_spider()

if __name__ == '__main__':
    streamListener = RetweetLDJAM()
    twitterStream = tweepy.Stream(auth,streamListener)
    twitterStream.filter(track=['LDJAM'])