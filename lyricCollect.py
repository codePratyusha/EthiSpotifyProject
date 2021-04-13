import lyricsgenius
# Make HTTP requests
import requests
# Scrape data from an HTML document
from bs4 import BeautifulSoup
# I/O
import os
# Search and manipulate strings
import re
GENIUS_ACCESS_TOKEN = 'BY9kWBApbyM6fFQIA-xga1oJkMN_uwKRXm8bL-CogSGr-HV6JywdlO9EUPmaslbs'
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
import pandas as pd  

#Change ID, Secret, etc
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="b6a1bd35934d45d2b42c19ef6b7b6c55",
                                               client_secret="68ca1e1105a943cf89f2c7e11ac599eb",
                                               redirect_uri="http://localhost/",
                                               scope = 'user-top-read'))

genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)

#artist = genius.search_artist("Post Malone", max_songs=3, sort="title")
#artist.save_lyrics()

allMusic = []

results = sp.current_user_top_tracks()

for i, item in enumerate(results['items']):
    allMusic+=[[item['artists'][0]['name'],item['name']]]
    #print(item['artists'][0]['name'],item['name'])

def scrape_song_lyrics(artistName, songTitle):
    vals = artistName.split() + songTitle.split()
    count = 1
    urlend = ''
    for x in vals:
        urlend+=x
        urlend+='-'
    urlend+='lyrics'

    url = 'https://genius.com/'+urlend
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    try:
        lyrics = html.find('div', class_='lyrics').get_text()
        #remove identifiers like chorus, verse, etc
        lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
        #remove empty lines
        lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])         
        return lyrics
    except:
        return ""

text = ""
f = open("myfile.txt", "w")
for pair in allMusic:
    text+=scrape_song_lyrics(pair[0], pair[1])
    f.write(scrape_song_lyrics(pair[0], pair[1]))
f.close()

with open('myfile.txt', 'r') as file:
    paragraph = file.read().replace('\n', '')

paragraph=paragraph.strip()

def readwords(filename):
    f = open(filename)
    words = [ line.rstrip() for line in f.readlines()]
    return words

positive = readwords('positive-words.txt')
negative = readwords('negative-words.txt')

count = Counter(paragraph.split())

pos = 0
neg = 0
for key, val in count.items():
    key = key.rstrip('.,?!\n') # removing possible punctuation signs
    if key in positive:
        pos += val
    if key in negative:
        neg += val

tot = pos + neg
print("Total sentiment words found:",tot)
print("Percent positive words found:",round((pos/tot)*100, 2))
print("Percent negative words found:",round((neg/tot)*100,2))

#print(scrape_song_lyrics('RL Grime',"92 Explorer"))
#https://genius.com/Post-malone-40-funk-lyrics