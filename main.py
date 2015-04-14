import os
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

# ld_number = 'ludum-dare-31'
ld_number = 'minild-58'

def ld_spider():
    url = get_random_entries_page()
    source_code = requests.get(url)
    text = source_code.text
    soup = BeautifulSoup(text)

    # get all td's -> items on the grid
    tds = soup.find_all('td')

    # get a random n from all the tds
    index = random.randrange(0,len(tds))

    # get the title of that item
    title = tds[index].find('i').string

    # get the url of that item
    url = 'http://ludumdare.com/compo/' + ld_number + '/' + tds[index].find('a').get('href')

    # get author of that item
    author = tds[index].img.contents[1]

    # download the first screenshot
    download_game_image(url)

    # prepare tweet string
    tweet = title + ' by ' + author + ' - ' + url

    # tweet!
    print('Tweeting: ' + tweet)
    api.update_with_media('img.jpg', tweet)

    # append_to_data(url)

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
    
    print('Page: ' + page_link)
    return page_link

# SAVE ALL THE TWEETED ENTRIES TO PREVENT DUPLICATES
def append_to_data(url):
    fw = open('data.txt', 'a')
    # text = 

    if url not in text:
        fw.write(str(x) + '\n')



# START BOT
ld_spider()