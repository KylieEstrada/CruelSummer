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

# Get Taylor Swift's artist ID
artist_name = "Taylor Swift"
results = sp.search(q='artist:' + artist_name, type='artist')
items = results['artists']['items']

if len(items) > 0:
    taylor_swift = items[0]
    taylor_swift_id = taylor_swift['id']

    # Get all Taylor Swift albums
    albums = []
    results = sp.artist_albums(taylor_swift_id, album_type='album')
    for album in results['items']:
        album_id = album['id']
        album_name = album['name']
        album_type = album['album_type']
        album_release_date = album['release_date']
        album_artists = []
        for artist in album['artists']:
            album_artists.append(artist['name'])
        albums.append({'id': album_id, 'name': album_name, 'type': album_type, 'release_date': album_release_date,
                       'artists': album_artists})

        # Get all tracks and audio features from each album
        tracks = []
        results = sp.album_tracks(album['id'])
        for track in results['items']:
            track_id = track['id']
            track_uri = track['uri']
            track_name = track['name']
            track_artists = []
            for artist in track['artists']:
                track_artists.append(artist['name'])
            tracks.append({'id': track_id, 'uri': track_uri, 'name': track_name, 'artists': track_artists})

else:
    print(f"No artist found for {artist_name}")

# Create a dataframe using pandas
