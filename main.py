import spotipy
from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

load_dotenv()

# Set up authentication
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to look up artist and return their tracks
def artist_tracks(artist_name):
    # Get artist ID
    artist_lookup = sp.search(q='artist:' + artist_name, type='artist')['artists']['items']

    # Checking if artist exists
    if len(artist_lookup) > 0:
        artist = artist_lookup[0]
    else:
        print(f"No artist found for {artist_name}")

    # Get all albums
    albums = []
    album_lookup = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(album_lookup['items'])
    while album_lookup['next']:
        album_lookup = sp.next(album_lookup)
        albums.extend(album_lookup['items'])

    albums.sort(key=lambda album: album['release_date'].lower())

    # Get all tracks
    tracks = []
    for album in albums:
        track_lookup = sp.album_tracks(album['id'])
        tracks.extend(track_lookup['items'])
        while track_lookup['next']:
            track_lookup = sp.next(track_lookup)
            tracks.extend(track_lookup['items'])

    return tracks

# Create a dataframe and export as csv
ts_tracks = artist_tracks("Taylor Swift")
ts_df = pd.DataFrame.from_dict(ts_tracks)
