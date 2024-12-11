import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3
from datetime import datetime

def lambda_handler(event, context):
    ##Spotify API
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    
    ##Extract playlist data
    artist_link = "https://open.spotify.com/artist/0TnOYISbd1XYRBk9myaseg"
    artist_url = artist_link.split('/')[-1].split('?')[0]

    data = sp.artist_top_tracks(artist_url)
    client = boto3.client('s3')
    filename = "spotify_raw_" + str(datetime.now()) + ".json"
    
    ## Save data into this folder
    client.put_object(
        Bucket="spotify-data-scrapping",
        Key="raw-data/to_process/" + filename,
        Body=json.dumps(data)
        )