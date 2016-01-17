import exifread
import os


class TweetS3Images(object):
    def __init__(self, twitter, s3_client):
        self._twitter = twitter
        self._s3_client = s3_client
        self._file = None

    def send_image(self, bucket, image_name, cleanup=False):
        temp_file = '/tmp/{}'.format(image_name)
        self._s3_client.download_file(bucket, image_name, temp_file)
        self._file = open(temp_file, 'rb')
        tags = exifread.process_file(self._file)
        status = self.get_image_description(tags, image_name)

        self._twitter.update_with_media(filename=image_name, status=status, file=self._file)

        if cleanup:
            self.cleanup(temp_file)

    def get_file(self):
        return self._file

    @staticmethod
    def cleanup(file_to_remove):
        os.remove(file_to_remove)

    @staticmethod
    def get_image_description(tags, image_name):
        if 'Image ImageDescription' in tags:
            description = tags['Image ImageDescription'].values
            status = (description[:100] + '..') if len(description) > 100 else description
        else:
            status = 'New image {} brought to you by lambda-tweet'.format(image_name)

        return status
