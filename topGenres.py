import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd  

#Change ID, Secret, etc
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="b6a1bd35934d45d2b42c19ef6b7b6c55",
                                               client_secret="68ca1e1105a943cf89f2c7e11ac599eb",
                                               redirect_uri="http://localhost/",
                                               scope = 'user-top-read'))

#get the genres for a specific artist
def genreFind(artist):
    result = sp.search(artist)
    track = result['tracks']['items'][0]
    artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
    #print(track['artists'][0]['name']," genres: ",artist["genres"])
    return [track['artists'][0]['name'],artist["genres"]]

#can control the amount of track returned:
#current_user_top_tracks(limit=20, offset=0, time_range='medium_term')

results = sp.current_user_top_tracks()

df = pd.DataFrame(columns = ["Artist", "Genres"]) 

topArtistGenres = []
for i, item in enumerate(results['items']):
    topArtistGenres+=genreFind(item['artists'][0]['name'])
df = pd.DataFrame(topArtistGenres) 
df.to_csv('data.csv')

'''for idx, item in enumerate(results['items']):
    track = item['track']
    #topTrack(track['artists'][0]['id'])
    genreFind(track['artists'][0]['name'])
    #print(idx, track['artists'][0]['name'], " – ", track['name'])

def topTrack(artist_id):
    results = sp.artist_top_tracks(artist_id, country='US')
    for track in results['tracks'][:10]:
        print('track    : ' + track['name'])
        print('audio    : ' + track['preview_url'])
        print('cover art: ' + track['album']['images'][0]['url'])
        print()
print(sp.recommendation_genre_seeds())

for idx, item in enumerate(results['items']):
    track = item['track']
    #topTrack(track['artists'][0]['id'])
    print(idx, track['artists'][0]['name'], " – ", track['name'])


results2 = sp.artist_top_tracks(artist_id, country='US')
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])'''
