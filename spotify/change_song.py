import json
import logging
import os

import boto3
from requests_oauthlib import OAuth2Session

# set up logging
logger = logging.getLogger('PySpotify')


def fetch_token():
    """ reads the client oauth token from S3 """
    bucket = os.environ["SPOTIFY_BUCKET_NAME"]
    path = os.getenv("SPOTIFY_BUCKET_PATH", "")
    logger.info("Reading Spotify OAuth token from s3://%s/%s/token.json." %
                (bucket, path))
    s3 = boto3.client('s3')
    content_object = s3.get_object(Bucket=bucket, Key="%s/token.json" % path)
    file_content = content_object['Body'].read().decode('utf-8')
    token = json.loads(file_content)
    return token


def save_token(token):
    """ saves a client oauth token to S3 """
    logger.info("Saving token to S3.")
    bucket = os.environ["SPOTIFY_BUCKET_NAME"]
    path = os.getenv("SPOTIFY_BUCKET_PATH", "")
    s3 = boto3.client('s3')
    data = json.dumps(token)
    s3.put_object(Bucket=bucket, Key="%s/token.json" % path, Body=data)
    return


def play_song(event, context):
    """ fetch a oauth protected url """
    print("event:", event)
    logger.info("Working on uri: %s")
    token = fetch_token()
    token_uri = 'https://accounts.spotify.com/api/token'
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    device_name = os.environ["DEVICE_NAME"]
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    extra = {'client_id': client_id, 'client_secret': client_secret}

    client = OAuth2Session(client_id, token=token,
                           auto_refresh_url=token_uri,
                           auto_refresh_kwargs=extra,
                           token_updater=save_token)

    base_uri = "https://api.spotify.com/v1/me/player/play"
    uri = base_uri

    r = client.get("https://api.spotify.com/v1/me/player/devices")
    data = r.json()
    print(data)

    if data and "devices" in data.keys():
        device_id = next(d for d in data['devices'] if d['name'] == device_name)['id']
        if device_id:
            uri = base_uri + "?device_id=" + device_id

    track = 'spotify:track:57frqbj2ilPbr9BIZzmkFl'
    if "track_arn" in event:
        track = event["track_arn"]

    print("Calling uri:" + uri)
    r = client.put(uri,
                   data=json.dumps({'uris': [track]}),
                   headers={'Content-Type': 'application/json',
                            'Accept': 'application/json'})
    r.status_code
    print(r)
    return json.dumps({})


if __name__ == "__main__":
    play_song({}, {})
