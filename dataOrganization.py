import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import json

cid = 'd7ef747707434c259054733b6defab05'
secret = '3a4ae1a96ac24674b1eb14ba39fbacc8'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def playlistReader(data):
    uriList = []
    for song in data:
        uriList.append(findID(song[1], song[0])[2][0])
    
    return uriList

def findID(artist, track):
    artist_name = []
    track_name = []
    track_id = []

    track_results = sp.search(q=f'artist:{artist}, track:{track}', type='track', limit=1)
    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])

    return artist_name, track_name, track_id

def yearURIs(year):
    artist_name = []
    track_name = []
    track_id = []

    track_results = sp.search(q=f'year:{year}', type='track', limit=50)
    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])

    return artist_name, track_name, track_id


def buildDataFrame(uris, indexNames):
    jsonSongs = sp.audio_features(uris)
    df = pd.DataFrame(data = jsonSongs, index = indexNames)
    return df.drop(columns = ["type", "id", "uri", "track_href", "analysis_url", "time_signature"])