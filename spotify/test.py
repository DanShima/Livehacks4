import json

import boto3

payload = json.dumps({"track_arn": "spotify:track:5lRtoB4Gg2gpT1EjAWOui7"})
session = boto3.Session(profile_name='serverless')
client = session.client('lambda', region_name='eu-west-1')
esponse = client.invoke(FunctionName='moodSpotify-dev-playSong', Payload=payload, )

print(esponse)
