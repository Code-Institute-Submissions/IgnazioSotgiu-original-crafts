from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

# code taken from code institute lecture


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION


class StaticMediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
