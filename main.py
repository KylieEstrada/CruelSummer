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

    # Checking if artist exists and assigns
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

    # Get all tracks
    tracks = []
    for album in albums:
        track_lookup = sp.album_tracks(album['id'])
        tracks.extend(track_lookup['items'])
        while track_lookup['next']:
            track_lookup = sp.next(track_lookup)
            tracks.extend(track_lookup['items'])

    return tracks

def all_song_data(tracks):
    track_data = []
    for i in tracks:
        track_info = sp.track(i['id'])
        features = sp.audio_features(i['id'])

        name = track_info['name']
        album = track_info['album']['name']
        artist = track_info['album']['artists'][0]['name']
        release_date = track_info['album']['release_date']
        duration_ms = track_info['duration_ms']
        popularity = track_info['popularity']

        acousticness = features[0]['acousticness']
        danceability = features[0]['danceability']
        energy = features[0]['energy']
        instrumentalness = features[0]['instrumentalness']
        liveness = features[0]['liveness']
        loudness = features[0]['loudness']
        speechiness = features[0]['speechiness']
        tempo = features[0]['tempo']
        time_signature = features[0]['time_signature']


        track = [name, album, artist, release_date, duration_ms, popularity, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
        track_data.append(track)

    return track_data

def create_csv(artist_name):
    tracks = artist_tracks(artist_name)
    track_data = all_song_data(tracks)
    df = pd.DataFrame(track_data, columns=['song', 'album', 'artist', 'release_date', 'duration_ms', 'popularity',
                                              'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness',
                                              'loudness', 'speechiness', 'tempo', 'time_signature'])
    df.to_csv(f'{artist_name}_songs.csv', index=False)

create_csv("Taylor Swift")
