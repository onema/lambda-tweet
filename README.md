lambda-tweet
============

Summary
-------

Sample AWS Lambda application written in python to tweet images that have been uploaded to an S3 bucket.
 
Requirements
------------
This lambda function assumes it has access to a file called `config.json` which has an entry called `secrets`.
Secrets is a json object that has been encrypted using AWS KMS and base64 encoded. The secrets has the 
following structure:
 
```
{
    'consumer-key': 'Twitter API consumer key',
    'consumer-secret': 'Twitter API consumer secret',
    'access-token': 'Twitter API access token', 
    'access-token-secret': Twitter API access token secret'
}
```
 
Usage
------
The bulk of the logic to send the image to twitter lives in the TweetS3Images class. This class requires a 
tweepy API object and a boto3 S3 client. 

You can use it like such:

```
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
boto_session = boto3.session.Session(profile_name='mindtouch', region_name='us-west-2')
client = boto_session.client('s3')

tweet_images = TweetS3Images(api, client)
tweet_images.send_image('juant-test', 'image.jpg')
```
