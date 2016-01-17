import os
import shutil
from unittest import TestCase
from mock import MagicMock
import tweepy
import boto3
from tweepy.models import Status
from tweet_s3_images import TweetS3Images


class TweetS3ImagesTest(TestCase):
    def test_sending_images(self):
        # ensure there is an image as the mock object will not do anything
        shutil.copy('./image.jpg', '/tmp/image.jpg')
        client = boto3.client('s3')
        client.download_file = MagicMock(return_value=None)

        auth = tweepy.OAuthHandler('foo', 'bar')
        api = tweepy.API(auth)
        api.update_with_media = MagicMock(return_value=Status())

        tweet_images = TweetS3Images(api, client)
        tweet_images.send_image('test_bucket', 'image.jpg', cleanup=True)

        client.download_file.assert_called_with('test_bucket', 'image.jpg', '/tmp/image.jpg')
        api.update_with_media.assert_called_with(
                filename='image.jpg',
                status='New image image.jpg brought to you by lambda-tweet',
                file=tweet_images.get_file())
        self.assertFalse(os.path.exists('/tmp/image-test.jpg'), 'The image was not cleaned up correctly.')
