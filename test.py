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

ld_number = 'ludum-dare-32'
# ld_number = 'minild-58'

def ld_spider():
    print("Crawling...")
    page_url = get_random_entries_page()
    source_code = requests.get(page_url)
    text = source_code.text
    soup = BeautifulSoup(text)

    # get all td's -> items on the grid
    tds = soup.find_all('td')

    # get a random n from all the tds
    index = random.randrange(0,len(tds))

    # get the url of that item
    url = 'http://ludumdare.com/compo/' + ld_number + '/' + tds[index].find('a').get('href')
    # url = 'http://ludumdare.com/compo/ludum-dare-32/?action=preview&uid=52764'
    # url = 'http://ludumdare.com/compo/ludum-dare-32/?action=preview&uid=25961'

    if game_already_tweeted(url):
        print('Already exists: ' + url)
        ld_spider()
    else:
        print('Preparing tweet...')
        # get author of that item
        author = tds[index].img.contents[1]

        # download the first screenshot
        download_game_image(url)

        # prepare tweet string
        tweet = makeTweet(author, url)

        # tweet!
        # tweetStatus = api.update_with_media('img.jpg', tweet)

        # fw = open('data.txt', 'a')
        # fw.write(str(url) + '\n')
        print("---")


def makeTweet(author, url):
    code = requests.get(url)
    text = code.text
    soup = BeautifulSoup(text)

    title = soup.findAll(attrs={'name' : 'twitter:title'})[1].get('content')

    twitterHandle = ''
    twitterUser = ''
    twitterUrl = ''

    if soup.findAll(attrs={'name' : 'twitter:creator'}):
        twitterHandle = soup.findAll(attrs={'name' : 'twitter:creator'})[0].get('content')

        twitterUser = twitterHandle

        if 'http://twitter.com/' in twitterHandle:
            twitterUser = twitterHandle.replace("http://twitter.com/", "")
        elif 'https://twitter.com/' in twitterHandle:
            twitterUser = twitterHandle.replace("https://twitter.com/", "")
        elif 'http://www.twitter.com/' in twitterHandle:
            twitterUser = twitterHandle.replace("http://www.twitter.com/", "")
        elif 'https://www.twitter.com/' in twitterHandle:
            twitterUser = twitterHandle.replace("https://www.twitter.com/", "")

        twitterUser = twitterUser.replace("@", "")

        twitterUrl = ' - (http://twitter.com/' + twitterUser + ')'

    tweet = prepareTweet(title, author, twitterUser, url)

    print(time.strftime("%m/%d/%Y %I:%M %p") + '\n' + title + ' by ' + author + twitterUrl + '\nLD Entry Page: ' + url)
    Notifier.notify(title + ' by ' + author + twitterHandle, contentImage='img.jpg', appIcon='pp.png', title='@LDJAMBot', open='http://twitter.com/ldjambot')
    
    return tweet

def prepareTweet(title, author, twitterUser, url):
    if twitterUser != '':
        author = '@' + twitterUser

    tweet = title + ' by ' + author + ' - ' + url + ' #LDJAM #gamedev #indiedev' 
    print('Tweet: ' + tweet)

    # TRIM IF > 140 CHARACTERS    
    if len(tweet) > 140:
        charactersToTrim = len(tweet) - 137
        title = title[:-charactersToTrim] + '...'
        tweet = title + ' by ' + author + twitterHandle + ' - ' + url + ' #LDJAM #gamedev #indiedev' 

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

# START BOT
ld_spider()