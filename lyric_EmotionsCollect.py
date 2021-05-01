import csv
import lyricsgenius
# Make HTTP requests
import requests
# Scrape data from an HTML document
from bs4 import BeautifulSoup
# I/O
import os
# Search and manipulate strings
import re
GENIUS_ACCESS_TOKEN = 'pjkvI4dkVl9VfaLMu0_rQGDj3JXeQLA2Fu1ldffVXLz1AtVJ9Y8KjU8MiA2xYWn0'

from collections import Counter
import pandas as pd  


#Sentiment analysis toolkits 
from nltk.tokenize import RegexpTokenizer
from nltk .stem import WordNetLemmatizer
from stop_words import get_stop_words
from nrclex import NRCLex


genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)
tokenizer = RegexpTokenizer(r'\w+')


#fn that reads a txt file with artistName,songName, trackID on each line and saves them into separate lists
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
        x[0] = re.sub('&', 'and', x[0])
        x[1] = re.sub('&', 'and', x[1])
        #store artist and song names in separate lists
        artistName.append(x[0])
        songName.append(x[1])
        trackID.append(x[2])
    #check all lines have been read
    print("Lines been read: ", count)
    return artistName, songName , trackID
    
        

#fn to scrape song lyrics, given artist name and song title 
def scrape_song_lyrics(artistName, songTitle):
    vals = artistName.split() + songTitle.split() 
    count = 1
    urlend = ''
    for x in vals:
        urlend+=x
        urlend+='-'
    urlend+='lyrics'

    url = 'https://genius.com/'+urlend
    print(url)
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    try:
        lyrics = html.find('div', class_='lyrics').get_text()
        #remove identifiers like chorus, verse, etc
        lyrics = re.sub('[\(\[].*?[\)\]]', '', lyrics)
        #remove empty lines
        lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])  
        #print(lyrics)       
        return lyrics
    except:
        print("no return from API")
        return ""



#fn to return [artistName, songName, positive, negative, anger, anticipation, disgust, fear, joy, sadness, surprise, trust ] for each song
def lyrics_to_emotions(artistName, songName, songLyrics, trackID):

    if songLyrics == "":
        return [artistName, songName, trackID, None, None, None, None, None, None, None, None, None, None]

    #init emotion values
    positive = negative = anger = anticipation = disgust = fear = joy = sadness = surprise = trust = 0

    #init counter for emotions
    positive_cnt = negative_cnt = anger_cnt = anticipation_cnt = disgust_cnt = fear_cnt = joy_cnt = sadness_cnt = surprise_cnt = trust_cnt = 0

    if songLyrics == "":
        return [artistName, songName, anger, anticipation, disgust, fear, joy, sadness, surprise, trust]

    #clean and tokenize lyrics str 
    #tokenization segments song lyrics into atomic elements
    raw = songLyrics.lower()
    tokens = tokenizer.tokenize(songLyrics)

    #create English stop words list
    en_stop = get_stop_words('en')

    #remove stop words from tokens
    #creates a list of tokens w/o stop words
    stopped_tokens = [i for i in tokens if not i in en_stop]
    print('Stopped')
    print(stopped_tokens)

    #lemmatize tokens
    wnl = WordNetLemmatizer()
    lem_tokens = [wnl.lemmatize(word) for word in stopped_tokens]

    #remove one-two letter tokens 
    lem_tokens = [word for word in lem_tokens if len(word)>2]

    print("lem_tokens")
    print(lem_tokens)


    for item in lem_tokens:
        #for each tokenized word, evaluate emotions
        emotion = NRCLex(item)
        #extract emotions with non-zero values
        for j in range(len(emotion.top_emotions)):
            if emotion.top_emotions[j][1] != 0:
                print("word: ", item, emotion.top_emotions[j][0], "score: ", emotion.top_emotions[j][1] )
                #update appropriate emotion with amount 
                if emotion.top_emotions[j][0] == 'positive':
                    #update positive
                    positive += emotion.top_emotions[j][1]
                    positive_cnt+=1
                    if positive_cnt > 0 :
                        positive = positive/positive_cnt 
                elif emotion.top_emotions[j][0] == 'negative':
                    #update negative
                    negative += emotion.top_emotions[j][1]
                    negative_cnt+=1
                    if negative_cnt > 0 :
                        negative = negative/negative_cnt 
                elif emotion.top_emotions[j][0] == 'anger':
                    #update anger
                    anger += emotion.top_emotions[j][1]
                    anger_cnt+=1
                    if anger_cnt > 0 :
                        anger = anger/anger_cnt 
                elif emotion.top_emotions[j][0] == 'anticipation':
                    #update anticipation
                    anticipation += emotion.top_emotions[j][1]
                    anticipation_cnt+=1
                    if anticipation_cnt > 0: 
                        anticipation = anticipation/anticipation_cnt 
                elif emotion.top_emotions[j][0] == 'disgust':
                    #update disgust
                    disgust += emotion.top_emotions[j][1]
                    disgust_cnt+=1
                    if disgust_cnt > 0:
                        disgust = disgust/disgust_cnt 
                elif emotion.top_emotions[j][0] == 'fear':
                    #update fear
                    fear += emotion.top_emotions[j][1]
                    fear_cnt+=1
                    if fear_cnt > 0:
                        fear = fear/fear_cnt  
                elif emotion.top_emotions[j][0] == 'joy':
                    #update joy
                    joy += emotion.top_emotions[j][1]
                    joy_cnt+=1
                    if joy_cnt > 0:
                        joy = joy/joy_cnt 
                elif emotion.top_emotions[j][0] == 'sadness':
                    #update sadness
                    sadness += emotion.top_emotions[j][1]
                    sadness_cnt+=1
                    if sadness_cnt > 0:
                        sadness = sadness/sadness_cnt 
                elif emotion.top_emotions[j][0] == 'surprise':
                    #update surprise
                    surprise += emotion.top_emotions[j][1]
                    surprise_cnt+=1
                    if surprise_cnt > 0:
                        surprise= surprise/surprise_cnt 
                elif emotion.top_emotions[j][0] == 'trust':
                    #update trust
                    trust += emotion.top_emotions[j][1]
                    trust_cnt+=1
                    if trust_cnt > 0:
                        trust= trust/trust_cnt 

    #ENDOF extracting emotions from songLyrics  
    # print("positive : ", positive, "positive_cnt: ", positive_cnt)
    # print("negative : ", negative, "negative_cnt: ", negative_cnt)
    # print("anger : ", anger, "anger_cnt: ", anger_cnt)
    # print("anticipation : ", anticipation, "anticipation_cnt: ", anticipation_cnt)
    # print("disgust: ", disgust, "disgust_cnt: ", disgust_cnt)
    # print("fear: ", fear, "fear_cnt: ", fear_cnt)
    # print("joy: ", joy, "joy_cnt: ", joy_cnt)
    # print("sadness: ", sadness, "sadness_cnt: ", sadness_cnt)
    # print("surprise: ", surprise, "surprise_cnt: ", surprise_cnt)
    # print("trust: ", trust, "trust_cnt: ", trust_cnt)

    return [artistName, songName, trackID, positive, negative, anger, anticipation, disgust, fear, joy, sadness, surprise, trust]




#ensure you cd into right directory
#open file
artistAndSong_file = open("artistAndSongName.txt",'r',encoding = 'utf-8') 
artistName, songTitle, trackID = text_to_list(artistAndSong_file)
    #read lines in file 
    #Lines = artistAndSong_file.readlines()
    #save artists and songs from file into separate lists
    #for line in Lines:
        #print(line)
        #print("artist: ", artistName)
#print(songTitle)

#close file
artistAndSong_file.close()

#create row to be column names
#row_list = []
col_names = ['Artist', 'Track', 'Track ID','Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust']
#row_list.append(col_names)

#create csv file of col rows
with open('emotions_from_lyrics.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(col_names)
file.close()

#fn to append list as rows

#extract lists of emotions from all songs as rows
#realized that some of the API calls to lyricsgenius fail
#to account for this, we try to scrape lyrics atleast 5 times before moving on from song
#we assume that if 5 API calls have failed, then the song lyrics aren't on Genius 
for i in range(0, len(artistName)):
    count=0 
    songLyrics = ""
    while(songLyrics == "" and count <5):
        songLyrics = scrape_song_lyrics(artistName[i], songTitle[i])
        count+=1
        #print("sl")
        #print(songLyrics)
        #print("endsl")
    print("scrape attempts: ", count, " for song: ", songTitle[i])
    row = lyrics_to_emotions(artistName[i], songTitle[i], songLyrics, trackID[i])
    print(row)
    #append row to row_list
    #row_list.append(row)
    #write row to csv file 
    with open('emotions_from_lyrics.csv', 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)
    file.close()   
#










# for i in range(len(artistName)):
#     try:
#         #pull song lyrics for each song
#         lyrics = scrape_song_lyrics(artistName[i], songName[i])

#         #extract emotions from lyrics
#         csv_row = lyrics_to_emotions(artistName[i], songName[i], lyrics)

#     except:
#         return []


#Testing lyrics_to_emotions ()

#lyrics_to_emotions('Taylor Swift', 'cardigan')