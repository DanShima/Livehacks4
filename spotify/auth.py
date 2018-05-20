#!/bin/env python

import logging
import os

import boto3
from requests_oauthlib import OAuth2Session

import change_song as spot

# set up logging
logger = logging.getLogger('PySpotify')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - ' +
                              '%(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

if __name__ == "__main__":
    client = boto3.client('ssm')
    """ interactive authorization helper """
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    # a bogus redirect uri
    redirect_uri = "https://localhost"

    # the scope required for our API requests
    scope = r'user-read-playback-state user-modify-playback-state user-read-currently-playing'

    # Request URLs for Spotify
    request_authorization_url = "https://accounts.spotify.com/authorize"
    request_token_url = "https://accounts.spotify.com/api/token"

    # create our oauth client
    oauth = OAuth2Session(client_id=client_id,
                          scope=scope,
                          redirect_uri=redirect_uri)

    authorization_url, state = oauth. \
        authorization_url(request_authorization_url)

    print('Go to %s and authorize access.' % authorization_url)

    authorization_response = input('Paste the full returned URL here: ')
    print("Auth response URL: '%s'" % authorization_response)

    token = oauth.fetch_token(
        request_token_url,
        client_secret=client_secret,
        authorization_response=authorization_response)

    bucket = os.getenv("SPOTIFY_BUCKET_NAME")
    spot.save_token(token)
