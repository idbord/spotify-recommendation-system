import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
cid = 'd7ef747707434c259054733b6defab05'
secret = '3a4ae1a96ac24674b1eb14ba39fbacc8'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



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


def readFile(path):
    f = open(path)
    result = []
    for line in f.readlines():
        result.append(line[:-1].split(","))

    return result

x = readFile("./songs.csv")

for song in x:
    print(findID(song[1], song[0]))
