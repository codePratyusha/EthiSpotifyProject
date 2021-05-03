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
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from nltk .stem import WordNetLemmatizer
from gensim import corpora, models
import gensim


genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)
tokenizer = RegexpTokenizer(r'\w+')


##########################################################################################################
# FUNCTIONS 
##########################################################################################################

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


#fn that conducts LDA analysis on a list of song lyrics 
# @params: 
#   song_set : list of type str 
def get_theme(song_set):

    # list for tokenized documents in loop
    texts = []

    for song in song_set:
        # clean and tokenize song str - this removes spaces 
        #tokenization segments song lyrics into atomic elements
        raw = song.lower()
        tokens = tokenizer.tokenize(song)

        #create English stop words list
        en_stop = get_stop_words('en')

        #remove stop words from tokens
        #creates a list of tokens w/o stop words
        stopped_tokens = [i for i in tokens if not i in en_stop]
        

        #lemmatize tokens
        wnl = WordNetLemmatizer()
        lem_tokens = [wnl.lemmatize(word) for word in stopped_tokens]

        #remove one-two letter tokens 
        lem_tokens = [word for word in lem_tokens if len(word)>3]

        # add tokens to list
        texts.append(lem_tokens)
    #

    #construct document-term matrix
    # Dictionary() traverses through texts and assigns unique integer id to each unique token, while collecting word counts
    #print(dictionary.token2id) --- prints the unique ids for all tokens
    dictionary = corpora.Dictionary(texts)

    #convert dictionary to bag of words 
    #corpus = list of vectors equal to a number of documents 
    #corpus[0] gives vector of tuples for first document , tuples are (term ID, term frequency) pairs
    corpus = [dictionary.doc2bow(text) for text in texts]
    #print('corpus: ', corpus)


    #generate lda model 
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=4,id2word = dictionary, passes=100)
    results = ldamodel.print_topics(num_topics=4, num_words=3)

    return results



# print('results')
# print(results)
# print('results[0]')
# print(results[0])
# print('results[0][1]')
# print(results[0][1])
# words = results[0][1].split(" + ")
# print("words")
# print(words)
# print("words[0]")
# print(words[0])
# #replace every non-alphabet char with empty str
# words[0] = re.sub('[^A-Za-z]+', '', words[0])
# print("words[0] removed")
# print(words[0])


        













##########################################################################################################
# MAIN
##########################################################################################################

#get input file from console 
# filename is type str
filename =  input('Enter input file name: ')
print("Recieved input is: ", filename)
with open(filename) as input_file:
    #Retrieve lists of artistName, songTitle, and trackID 
    artistName, songTitle, trackID = text_to_list(input_file)
#close file 
input_file.close()

#create song list from all songs in input file 
song_set = []

#For each song in input file
for i in range(0, len(artistName)):
    #Get song lyrics - attempt to scrape lyrics atleast 5 times to account for API fails
    # Assume lyrics don't exist on Genius if scrape attempt fails 5 times
    count=0 
    songLyrics = ""
    while(songLyrics == "" and count <5):
        songLyrics = scrape_song_lyrics(artistName[i], songTitle[i])
        count+=1
        print("scrape attempts: ", count, " for song: ", songTitle[i])
    
    #append song lyrics to song_set
    song_set.append(songLyrics)
#

#print("len song_set: ", len(song_set))

#get themes using lda model
results = get_theme(song_set)

print('results')
print(results)
print('results[0]')
print(results[0])
print('results[0][1]')
print(results[0][1])
words = results[0][1].split(" + ")
print("words")
print(words)
print("words[0]")
print(words[0])
#replace every non-alphabet char with empty str
words[0] = re.sub('[^A-Za-z]+', '', words[0])
print("words[0] removed")
print(words[0])

















# #print(scrape_song_lyrics('Taylor Swift', 'cardigan'))

# #lyrics of type str
# #print(type(scrape_song_lyrics('Taylor Swift', 'cardigan')))

# #scrape song
# # song1 = scrape_song_lyrics('Taylor Swift', 'cardigan')
# # song2 = scrape_song_lyrics('Taylor Swift', 'Lover')
# #song3 = scrape_song_lyrics('Taylor Swift', 'betty')
# #song4 = scrape_song_lyrics('Taylor Swift', 'You Belong with Me')
# #song5 = scrape_song_lyrics('Taylor Swift', 'Love Story')

# # # compile sample songs into a list
# # song_set = [song1, song2]

# # # list for tokenized documents in loop
# # texts = []

# for song in song_set:
#     # clean and tokenize song str - this removes spaces 
#     #tokenization segments song lyrics into atomic elements
#     raw = song.lower()
#     tokens = tokenizer.tokenize(song)

#     #create English stop words list
#     en_stop = get_stop_words('en')

#     #remove stop words from tokens
#     #creates a list of tokens w/o stop words
#     stopped_tokens = [i for i in tokens if not i in en_stop]
#     print('Stopped')
#     print(stopped_tokens)


#     #stem words to reduce topically similar words to their roots (e.g. posing, poser --> pose )
#     #ensure all stopped_tokens are of type str
#     #stem all tokens
#     #using the PorterStemmer, the trailing 'e' for some words are removed, so we use the WordNetLemmatizer for words ending in 'e'
#     #stemmed_tokens = [wnl.lemmatize(word) if wnl.lemmatize(word).endswith('e') or wnl.lemmatize(word).endswith('y') else p_stemmer.stem(word) for word in stopped_tokens]

#     # add tokens to list
#     #texts.append(stemmed_tokens)
#     texts.append(stopped_tokens)

#     #texts = [p_stemmer.stem(i) for i in stopped_tokens]
#     #print('Stemmed')
#     #print(texts)


# print("For whole lyrics: START")
# for item in texts:
#     for i in range(len(item)):
#         emotion2 = NRCLex(item[i])
#         for j in range(len(emotion2.top_emotions)):
#             if emotion2.top_emotions[j][1] != 0:
#                 print('\n\n', item[i], ': ', emotion2.top_emotions[j][0], ': ', emotion2.top_emotions[j][1]) 
# print("For whole lyrics: END")

# # #construct document-term matrix
# # # Dictionary() traverses through texts and assigns unique integer id to each unique token, while collecting word counts
# # #print(dictionary.token2id) --- prints the unique ids for all tokens
# # dictionary = corpora.Dictionary(texts)
# # print('dictionary')
# # print(dictionary)
# # print(dictionary.token2id)
# # #convert dictionary to bag of words 
# #corpus = list of vectors equal to a number of documents 
# # corpus[0] gives vector of tuples for first document , tuples are (term ID, term frequency) pairs
# # corpus = [dictionary.doc2bow(text) for text in texts]
# # print('corpus')
# # print(corpus)
# # print(type(corpus))

# # #Best results with cardigan, lover, you belong with me, betty and love story: num_topics = 5, passes = 100, num_words = 10
# # ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=5 ,id2word = dictionary, passes=100)
# # #print(ldamodel.print_topics(num_topics=5, num_words=10))

# # results = ldamodel.print_topics(num_topics=5, num_words=10)
# # print('results')
# # print(results)
# # print('results[0]')
# # print(results[0])
# # print('results[0][1]')
# # print(results[0][1])
# # words = results[0][1].split(" + ")
# # print("words")
# # print(words)
# # print("words[0]")
# # print(words[0])
# # #replace every non-alphabet char with empty str
# # words[0] = re.sub('[^A-Za-z]+', '', words[0])
# # print("words[0] removed")
# # print(words[0])

# #exclude pronouns, 
# # exclude_words = ['i' , 'you', 'they', 'them', 'him', 'her', 'he', 'she', 'and' ]
# # #For each topic, split the results based on +
# # for i in range(len(results)):
# #     words = results[i][1]
# #     #separate words in topic
# #     words = words.split(" + ")
# #     #only keep part of the string between " "
# #     for item in words:
# #         item = re.sub('[^A-Za-z]+', '', item)
# #         #exclude 1 letter words, and other common words 
# #         if item not in exclude_words and len(item)>1:
# #             emotion = NRCLex(item)
# #             print('\n\n', item, ': ', emotion.top_emotions)
# #         #for each of those words
# #         # if word is not one letter, or "i", or "you", , conduct NRC lexicon analysis 
# #         #emotion = NRCLex


# # #NRC 



# #stem all the words
# # texts = []
# # for i in stopped_tokens:
# #     texts += p_stemmer.stem(i)

# # print('Stemmed')
# # print(texts)


# #To find a song by a certain artist 
# #artist = genius.search_artist('Taylor Swift', max_songs=1)

# #To find a specific song by a specific artist
# #song = genius.search_song(title = 'Finally Feel Good', artist = 'James Arthur')
# # print(song)


# #add song to artist 
# #artist.add_song(song)
# #print(artist)

# #print the song lyrics
# #print(artist.songs[0])
# #save song lyrics into json file
# #artist.save_lyrics()


# #read in a text file that has artist_name, song_name on each line 
# # read in each line
#     #split into artist_name str and song_name str by , 
#     #call scrape_song_lyrics (artist_name, song_name)




# artist_and_song_list = []




# # #artist_and_song list of elements [artist_name, song_name] of type list of str
# # for pair in artist_and_song_list:
# #     #split the element to get the artist and song name separately
# #     artist_name = pair[0]
# #     song_name = pair[1]

# #function that takes in an input of a str in the format 'artistname,songname' and returns them separately 
# #def get_artist_and_song()



# # #artist = genius.search_artist("Post Malone", max_songs=3, sort="title")
# # #artist.save_lyrics()

# # allMusic = []

# # for i, item in enumerate(results['items']):
# #     allMusic+=[[item['artists'][0]['name'],item['name']]]
# #     print(item['artists'][0]['name'],item['name'])























# # text = ""
# # f = open("myfile.txt", "w")
# # text+=scrape_song_lyrics('James Arthur', 'Finally Feel Good')
# # f.write(scrape_song_lyrics('James Arthur', 'Finally Feel Good'))
# # f.close()


# # # for pair in allMusic:
# #     text+=scrape_song_lyrics(pair[0], pair[1])
# #     f.write(scrape_song_lyrics(pair[0], pair[1]))
# # f.close()





# #  with open('myfile.txt', 'r') as file:
# #     paragraph = file.read().replace('\n', '')

# #  paragraph=paragraph.strip()



# # Positive negative analysis 


# # def readwords(filename):
# #     f = open(filename)
# #     words = [ line.rstrip() for line in f.readlines()]
# #     return words


# # positive = readwords('positive-words.txt')
# # negative = readwords('negative-words.txt')

# # count = Counter(paragraph.split())

# # pos = 0
# # neg = 0
# # for key, val in count.items():
# #     key = key.rstrip('.,?!\n') # removing possible punctuation signs
# #     if key in positive:
# #         pos += val
# #     if key in negative:
# #         neg += val

# # tot = pos + neg
# # print("Total sentiment words found:",tot)
# # print("Percent positive words found:",round((pos/tot)*100, 2))
# # print("Percent negative words found:",round((neg/tot)*100,2))

# #print(scrape_song_lyrics('RL Grime',"92 Explorer"))
# #https://genius.com/Post-malone-40-funk-lyrics