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

# ld_number = 'ludum-dare-32'
ld_number = 'minild-58'

def ld_spider():
    print("Tweeting...")
    url = get_random_entries_page()
    source_code = requests.get(url)
    text = source_code.text
    soup = BeautifulSoup(text)

    # get all td's -> items on the grid
    tds = soup.find_all('td')

    # get a random n from all the tds
    index = random.randrange(0,len(tds))

    # get the url of that item
    url = 'http://ludumdare.com/compo/' + ld_number + '/' + tds[index].find('a').get('href')

    if game_already_tweeted(url):
        print('Already exists: ' + url)
        ld_spider()
    else:
        # get the title of that item
        title = tds[index].find('i').string

        # get author of that item
        author = tds[index].img.contents[1]

        # download the first screenshot
        download_game_image(url)

        # prepare tweet string
        tweet = prepareTweet(title, author, url)

        # tweet!
        print(time.strftime("%m/%d/%Y %H:%M") + '\n' + title + ' by ' + author +' \n' + url)
        # api.update_with_media('img.jpg', tweet)
        # fw = open('data.txt', 'a')
        # fw.write(str(url) + '\n')
        Notifier.notify(title + ' by ' + author, contentImage='img.jpg', appIcon='pp.png', title='@LDJAMBot', open='http://twitter.com/ldjambot')
        print("---")

# PREPARE TWEET STRING, CUT TITLE IF > 140
def prepareTweet(title, author, url):
    tweet = title + ' by ' + author + ' - ' + url + ' #LDJAM #gamedev #indiedev'
    if len(tweet) > 140:
        charactersToTrim = len(tweet) - 137
        title = title[:-charactersToTrim] + '...'
        tweet = prepareTweet(title, author, url)
        print(len(tweet))
    
    return tweet


# DOWNLOAD FIRST SCREENSHOT IN A ENTRY PAGE
def download_game_image(game_url):
    code = requests.get(game_url)
    text = code.text
    soup = BeautifulSoup(text)

    # get image url of first screenshot thumbnail
    img_url = soup.find('div', id='shot-nav-0').find('img').get('src')

    # get the raw image from the cropped thumbnail
    img_url = img_url.replace('-crop-180-140.jpg', '')

    # download the image
    download_image(img_url)

# DOWNLOAD IMAGE URL
def download_image(img_url):
    name = 'img'
    full_name = str(name) + '.jpg'
    urllib.request.urlretrieve(img_url, full_name)

# GET A RANDOM "VIEW GAMES" PAGE
def get_random_entries_page():
    url = 'http://ludumdare.com/compo/' + ld_number + '/?action=preview&q=&etype=&start=0'
    source_code = requests.get(url)
    text = source_code.text
    soup = BeautifulSoup(text)

    # select a random page link from the page hrefs
    items = soup.find_all('div', {'id' : 'compo2'})[0].find_all('p')[2].find_all('a')
    page_link = 'http://ludumdare.com/compo/' + ld_number + '/' + items[random.randrange(0,len(items))].get('href')
    
    return page_link

# SAVE ALL THE TWEETED ENTRIES TO PREVENT DUPLICATES
def game_already_tweeted(url):
    fr = open('data.txt', 'r')
    text = fr.read()

    if url not in text:
        return False

    return True

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