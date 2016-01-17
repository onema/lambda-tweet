import boto3
import tweepy
import json
import base64
from tweet_s3_images import TweetS3Images

with open('./config.json', 'r') as file:
    config = json.loads(file.read())

    # Decrypt API keys
    client = boto3.client('kms')
    response = client.decrypt(CiphertextBlob=base64.b64decode(config['secrets']))
    secrets = json.loads(response['Plaintext'])
    CONSUMER_KEY = secrets['consumer-key']
    CONSUMER_SECRET = secrets['consumer-secret']
    ACCESS_TOKEN = secrets['access-token']
    ACCESS_TOKEN_SECRET = secrets['access-token-secret']


def lambda_handler(event, context):
    print('Received event: ' + json.dumps(event, indent=2))
    print()
    s3_info = event['Records'][0]['s3']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    client = boto3.client('s3')

    tweet_images = TweetS3Images(api, client)
    tweet_images.send_image(s3_info['bucket']['name'], s3_info['object']['key'], cleanup=True)
