import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import json
from math import *

# These codes are how we connect to the Spotify API
cid = 'd7ef747707434c259054733b6defab05'
secret = '3a4ae1a96ac24674b1eb14ba39fbacc8'

# Set to False to not print out whole data set, True to print the whole data set out
print_data_set = False

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def playlistReader(data):
    uriList = []
    track_name = []
    values = []
    for song in data:
        uriList.append(findID(song[1], song[0])[2][0])
        track_name.append(song[0])
        values.append(int(song[2]))
    return uriList, track_name, values


def playlistReaderCompare(data):
    uriList = []
    track_name = []
    for song in data:
        uriList.append(findID(song[1], song[0])[2][0])
        track_name.append(song[0])
    return uriList, track_name


# Uses the artist name and the name of the track to find the ID of the song in Spotify
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


# Finds the Artist, Track Name, URI, and Song information for the top 50 songs of the given year
def yearURIs(year):
    artist_name = []
    track_name = []
    track_id = []
    values = []

    track_results = sp.search(q=f'year:{year}', type='track', limit=50)
    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        values.append("Yes")

    return artist_name, track_name, track_id, values


def buildDataFrame(uris, indexNames, values):
    jsonSongs = sp.audio_features(uris)
    df = pd.DataFrame(data=jsonSongs, index=indexNames)
    df.loc[:, "Classification"] = values
    if print_data_set:
        pd.set_option('display.max_columns', None)  # Setting allows for entire dataset to be printed
    return df.drop(columns=["type", "id", "uri", "track_href", "analysis_url", "duration_ms", "time_signature"])


def buildDataFrameCompare(uris, indexNames):
    jsonSongs = sp.audio_features(uris)
    df = pd.DataFrame(data=jsonSongs, index=indexNames)
    if print_data_set:
        pd.set_option('display.max_columns', None)  # Allows for entire dataset to be printed
    return df.drop(columns=["type", "id", "uri", "track_href", "analysis_url", "time_signature"])


# Rounds the numeric values within the fields with some transformations, if needed.
def roundAndMapValues(dataframe):
    dataframe["danceability"] = [mapValues(round(i * 100, 0)) for i in dataframe["danceability"]]
    dataframe["energy"] = [mapValues(round(i * 100, 0)) for i in dataframe["energy"]]
    dataframe["loudness"] = [mapValues(round(i, 0)) for i in dataframe["loudness"]]
    dataframe["speechiness"] = [mapValues(round(i * 100, 0)) for i in dataframe["speechiness"]]
    dataframe["acousticness"] = [mapValues(round(i * 100, 0)) for i in dataframe["acousticness"]]
    dataframe["instrumentalness"] = [mapValues(round(i * 100, 0)) for i in dataframe["instrumentalness"]]
    dataframe["liveness"] = [mapValues(round(i * 100, 0)) for i in dataframe["liveness"]]
    dataframe["valence"] = [mapValues(round(i * 100, 0)) for i in dataframe["valence"]]
    dataframe["tempo"] = [mapValues(round(i, 0)) for i in dataframe["tempo"]]
    return dataframe


# Maps numeric values, according to a step function of tens
# (i.e. 0 -> -1, 1 - 9 -> 0, 10 - 19 -> 1)
def mapValues(num):
    num = abs(num)
    try:
        length = int(log10(num) + 1)

        if length == 1:
            return 0
        elif length == 2:
            return getDigit(1, num)
        else:
            return int(str(getDigit(2, num)) + str(getDigit(1, num)))
    except:
        return -1  # This value is assigned when the numerical value is equal to 0


# Returns wanted digit from a number
def getDigit(want, num):
    return int(num // 10 ** want % 10)
