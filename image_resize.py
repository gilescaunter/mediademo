import boto3

import uuid

from PIL import Image

COVER_SIZE = [200, 150]

s3_client = boto3.client('s3')


def image_cover(image_source_path, resized_cover_path):
    with Image.open(image_source_path) as image:
        image.thumbnail(COVER_SIZE)
        image.save(resized_cover_path, image.format)


def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        upload_path_cover = '/tmp/resized-{}'.format(key)

        s3_client.download_file(bucket, key, download_path)

        image_cover(download_path, upload_path_cover)
    s3_client.upload_file(upload_path_cover, '{bucket_name}cover'.format(bucket_name=bucket),
                          'cover-{key}'.format(key=key))

image_cover('blue.jpg','foo1.jpg')