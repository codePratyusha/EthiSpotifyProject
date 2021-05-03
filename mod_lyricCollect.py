import lyricsgenius
# Make HTTP requests
import requests
# Scrape data from an HTML document
from bs4 import BeautifulSoup
# I/O
import os
import csv
# Search and manipulate strings
import re


#Access GENIUS API 
GENIUS_ACCESS_TOKEN = 'pjkvI4dkVl9VfaLMu0_rQGDj3JXeQLA2Fu1ldffVXLz1AtVJ9Y8KjU8MiA2xYWn0'

from collections import Counter
import pandas as pd  

genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)

##########################################################################################################
# FUNCTIONS 
##########################################################################################################

#fn to scrape song lyrics, given artist name and song title 
# @params:
#    artistName : str 
#    songTitle : str 
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
        print("no return from API")
        return ""


#fn that takes each line of filename, 
# @params: 
#   filename: txt file 
def readwords(filename):
    f = open(filename)
    words = [ line.rstrip() for line in f.readlines()]
    return words


#fn that reads a txt file with artistName,songName, trackID on each line and saves them into separate lists
# @params: 
#     file: txt file

def text_to_list(file):
    artistName = []
    songName = []
    trackID = []
    count = 0

    for line in file:
        print("Line being read: ", line)
        count+=1
        #split line by comma 
        x = line.split(',')
        #replace & with "and" for artist names and song names
        print("x0: ", x[0])
        print("x1: ", x[1])
        print("x2: ", x[2])
        x[0] = re.sub('&', 'and', x[0])
        x[1] = re.sub('&', 'and', x[1])
        #store artist and song names in separate lists
        artistName.append(x[0])
        songName.append(x[1])
        trackID.append(x[2])
    #check all lines have been read
    print("Lines been read: ", count)
    return artistName, songName , trackID
    

##########################################################################################################
# MAIN
##########################################################################################################

#cd into correct directory 

#Read in positive and negative word dictionary 
positive = readwords('positive-words.txt')
negative = readwords('negative-words.txt')

#Get input file from console 
# filename is type str
filename =  input('Enter input file name: ')
print("Recieved input is: ", filename)
with open(filename) as input_file:
    #Retrieve lists of artistName, songTitle, and trackID 
    artistName, songTitle, trackID = text_to_list(input_file)
#close file 
input_file.close()

#create row to be col names for csv 
col_names = ['Input File','Percentage of Positive Words', 'Percentage of Negative Words']

#create csv file of col rows
filename = re.sub(".txt", "", filename)
results_file = filename + "_results.csv"

with open(results_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(col_names)
file.close()

#init 
total_pos = 0
total_neg = 0

#For each song in txt file: 
for i in range(0, len(artistName)):
    
    #init
    text = ""

    #Get song lyrics - attempt to scrape lyrics atleast 5 times to account for API fails
    # Assume lyrics don't exist on Genius if scrape attempt fails 5 times
    count=0 
    songLyrics = ""
    while(songLyrics == "" and count <5):
        songLyrics = scrape_song_lyrics(artistName[i], songTitle[i])
        count+=1
        print("scrape attempts: ", count, " for song: ", songTitle[i])
    
    #store song lyrics in songlyrics.txt (overwrite for each song)
    f = open("myfile.txt", "w")
    f.write(songLyrics)
    f.close()

    #clean songlyrics.txt
    with open('myfile.txt', 'r') as file:
         paragraph = file.read().replace('\n', ' ')
    
    paragraph=paragraph.strip()
    
    #count positive and negative words found in song 
    count = Counter(paragraph.split())

    pos = 0
    neg = 0
    for key, val in count.items():
        key = key.rstrip('.,?!\n') # removing possible punctuation signs
        if key in positive:
            pos += val
        if key in negative:
            neg += val

    #update total positive and total negative words 
    total_pos += pos
    total_neg += neg

    print("artist: ", artistName[i], "song: ", songTitle[i], "pos: ", pos, "neg: ", neg)

# count total words = total positive + total negative words
total_words = total_pos + total_neg 
# find % positive words
percent_positive = round((total_pos/total_words)*100, 2)

# find % negative words 
percent_negative = round((total_neg/total_words)*100,2)

#create row for csv
filename = re.sub("artistAndSongName_", "", filename)
row = [filename, percent_positive, percent_negative]

#append row to csv 
with open(results_file, 'a+', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(row)
file.close()   
#












#artist = genius.search_artist("Post Malone", max_songs=3, sort="title")
#artist.save_lyrics()

# allMusic = []

# results = sp.current_user_top_tracks()

# for i, item in enumerate(results['items']):
#     allMusic+=[[item['artists'][0]['name'],item['name']]]
#     #print(item['artists'][0]['name'],item['name'])



# text = ""
# f = open("myfile.txt", "w")
# for pair in allMusic:
#     text+=scrape_song_lyrics(pair[0], pair[1])
#     f.write(scrape_song_lyrics(pair[0], pair[1]))
# f.close()

# with open('myfile.txt', 'r') as file:
#     paragraph = file.read().replace('\n', '')

# paragraph=paragraph.strip()


# positive = readwords('positive-words.txt')
# negative = readwords('negative-words.txt')

# count = Counter(paragraph.split())

# pos = 0
# neg = 0
# for key, val in count.items():
#     key = key.rstrip('.,?!\n') # removing possible punctuation signs
#     if key in positive:
#         pos += val
#     if key in negative:
#         neg += val

# tot = pos + neg
# print("Total sentiment words found:",tot)
# print("Percent positive words found:",round((pos/tot)*100, 2))
# print("Percent negative words found:",round((neg/tot)*100,2))

# #print(scrape_song_lyrics('RL Grime',"92 Explorer"))
# #https://genius.com/Post-malone-40-funk-lyrics