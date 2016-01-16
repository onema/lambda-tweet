import exifread
import os


class TweetS3Images(object):
    def __init__(self, twitter, s3_client):
        self._twitter = twitter
        self._s3_client = s3_client
        self._file = None

    def send_image(self, bucket, image_name, cleanup=False):
        temp_file = './{}'.format(image_name)
        self._s3_client.download_file(bucket, image_name, temp_file)
        self._file = open(temp_file, 'rb')
        status = 'New image {}'.format(image_name)
        tags = exifread.process_file(self._file)

        self._twitter.update_with_media(filename=image_name, status=status, file=self._file)

        if cleanup:
            self.cleanup(temp_file)

    def get_file(self):
        return self._file

    def cleanup(self, file):
        os.remove(file)
