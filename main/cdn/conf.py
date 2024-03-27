import os

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'pcrprep'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
  'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'https://pcrprep.nyc3.digitaloceanspaces.com'

# User file input storage
DEFAULT_FILE_STORAGE = "main.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "main.cdn.backends.StaticRootS3Boto3Storage"
