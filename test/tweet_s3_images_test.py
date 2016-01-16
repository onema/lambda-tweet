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
        auth = tweepy.OAuthHandler('foo', 'bar')
        api = tweepy.API(auth)
        api.update_with_media = MagicMock(return_value=Status())

        client = boto3.client('s3')
        client.download_file = MagicMock(return_value=None)

        tweet_images = TweetS3Images(api, client)
        tweet_images.send_image('test_bucket', 'image.jpg')

        client.download_file.assert_called_with('test_bucket', 'image.jpg', './image.jpg')
        api.update_with_media.assert_called_with(
                filename='image.jpg',
                status='New image image.jpg',
                file=tweet_images.get_file())

    def test_sending_images_with_cleanup(self):
        shutil.copy('./image.jpg', './image-test.jpg')
        auth = tweepy.OAuthHandler('foo', 'bar')
        api = tweepy.API(auth)
        api.update_with_media = MagicMock(return_value=Status())

        client = boto3.client('s3')
        client.download_file = MagicMock(return_value=None)

        tweet_images = TweetS3Images(api, client)
        tweet_images.send_image('test_bucket', 'image-test.jpg', True)

        client.download_file.assert_called_with('test_bucket', 'image-test.jpg', './image-test.jpg')
        api.update_with_media.assert_called_with(
                filename='image-test.jpg',
                status='New image image-test.jpg',
                file=tweet_images.get_file())

        self.assertFalse(os.path.exists('./image-test.jpg'), 'The image was not cleaned up correctly.')
