# Spotify - Serverless integration

Trigger a song change in Spotify with a serverless function

## Setup environment

- Install [Serverless](https://serverless.com/framework/docs/providers/aws/guide/quick-start/)
- Install [Serverless Python Requirements plugin](https://github.com/UnitedIncome/serverless-python-requirements)
- Install [AWS cli](http://brewformulas.org/Awscli)
- Install python 3
- Install requirements (eventually with virtualenv) `pip install -r requirements.txt`


If you have multiple profiles, configure a new profile add a block in `~/.aws/credentials` that looks like:
```
[serverless]
aws_access_key_id = XXXXXXXXXX
aws_secret_access_key = XXXXXXXXXX
```


## Setup Spotify

- Create an app https://beta.developer.spotify.com/dashboard/login
- In the Spotify app settings fill in `https://localhost` as Redirect URIs
- Run `auth.py` in a terminal to provide [authorisation](https://beta.developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow)
```
SPOTIFY_CLIENT_ID=XXXXXXXXXX \
SPOTIFY_CLIENT_SECRET=XXXXXXXXXX \
SPOTIFY_BUCKET_NAME=XXXXXXXXXX \
python auth.py
```

## Add secrets to SSM Parameter Store

run the following commands in the terminal replacing XXXXXXXXXX with the actual values
```
# Spotify Client ID
aws ssm put-parameter --name spotyCliId --type String --value XXXXXXXXXX --profile serverless --region eu-west-1
# Spotify Client Secret
aws ssm put-parameter --name spotyCliSec --type String --value XXXXXXXXXX --profile serverless --region eu-west-1
# S3 bucket where the current Spotify auth tocken will be stored
aws ssm put-parameter --name spotyBucket --type String --value XXXXXXXXXX --profile serverless --region eu-west-1
# S3 bucket where the current Spotify auth tocken will be stored
aws ssm put-parameter --name deviceName --type String --value XXXXXXXXXX --profile serverless --region eu-west-1
```
The value can be updated with adding `--overwrite`
I use `--profile serverless because I have multiple profiles configured in `~/.aws/credentials`

## Running locally

run in the terminal
```
SPOTIFY_CLIENT_ID=XXXXXXXXXX \
SPOTIFY_CLIENT_SECRET=XXXXXXXXXX \
SPOTIFY_BUCKET_NAME=XXXXXXXXXX \
DEVICE_NAME=XXXXXXXXXX \
python change_song.py
```

## Deploying the lambda

Run in terminal
```
serverless deploy --aws-profile serverless
```
I use `--aws-profile serverless` because I have multiple profiles configured in `~/.aws/credentials`

## Invoke from terminal
Run
```
serverless invoke --function playSong --aws-profile serverless --region eu-west-1
```

## todo
- parametrise song
- refactor function

## References

- [Spotify authorisation](https://beta.developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow)
- [Spotify console](https://beta.developer.spotify.com/console)
- [Boto3](https://boto3.readthedocs.io/en/latest/guide/quickstart.html)
- [AWS cli](https://docs.aws.amazon.com/cli/latest/reference/)

## Credits
- Parts of this code was inspired by https://github.com/davidski/spotify-lambda
