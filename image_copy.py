#from __future__ import print_function

import boto3

import os
import sys
import uuid

from PIL import Image
#import PIL.Image
#from resizeimage import resizeimage

COVER_SIZE = [200, 150]
PROFILE_SIZE = [200, 200]
THUMBNAIL_SIZE = [250, 250]

s3_client = boto3.client('s3')


def image_cover(image_source_path, resized_cover_path):
    with Image.open(image_source_path) as image:
        image.thumbnail(COVER_SIZE)
        image.save(resized_cover_path, image.format)


def image_cover(image_source_path, resized_cover_path):
    with Image.open(image_source_path) as image:
        cover = resizeimage.resize_cover(image, COVER_SIZE)
        cover.save(resized_cover_path, image.format)


def image_profile(image_source_path, resized_cover_path):
    with Image.open(image_source_path) as image:
        profile = resizeimage.resize_cover(image, PROFILE_SIZE)
        profile.save(resized_cover_path, image.format)


def image_thumbnail(image_source_path, resized_cover_path):
    with Image.open(image_source_path) as image:
        thumbnail = resizeimage.resize_thumbnail(image, THUMBNAIL_SIZE)
    thumbnail.save(resized_cover_path, image.format)


def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        upload_path_cover = '/tmp/resized-{}'.format(key)
        upload_path_profile = '/tmp/resized-{}'.format(key)
        upload_path_thumbnail = '/tmp/resized-{}'.format(key)

        s3_client.download_file(bucket, key, download_path)

        image_cover(download_path, upload_path_cover)
    s3_client.upload_file(upload_path_cover, '{bucket_name}cover'.format(bucket_name=bucket),
                          'cover-{key}'.format(key=key))

    image_profile(download_path, upload_path_cover)
    s3_client.upload_file(upload_path_cover, '{bucket_name}profile'.format(bucket_name=bucket),
                          'profile-{key}'.format(key=key))

    image_thumbnail(download_path, upload_path_thumbnail)
    s3_client.upload_file(upload_path_thumbnail, '{bucket_name}thumbnails'.format(bucket_name=bucket),
                          'thumbnail-{key}'.format(key=key))

