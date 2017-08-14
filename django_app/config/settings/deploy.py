from .base import *

config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

DEBUG = False
ALLOWED_HOSTS = config_secret_deploy['django']['allowed_hosts']

DATABASES = config_secret_deploy['django']['database']

WSGI_APPLICATION = 'config.wsgi.deploy.application'

AWS_ACCESS_KEY_ID = config_secret_deploy['aws']['access_key_id']
AWS_SECRET_ACCESS_KEY = config_secret_deploy['aws']['secret_access_key']
AWS_STORAGE_BUCKET_NAME = config_secret_deploy['aws']['s3_bucket_name']
AWS_S3_REGION_NAME = config_secret_deploy['aws']['s3_region_name']
S3_USE_SIGV4=True

STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
STATICFILES_STORAGE = 'config.storages.StaticStorage'
MEDIA_URL='/media/'
STATIC_URL='/static/'

# Celery
CELERY_BROKER_URL = config_secret_deploy['aws']['elasticache']
CELERY_RESULT_BACKEND = config_secret_deploy['aws']['elasticache']
