from .base import *

config_secret_debug = json.loads(open(CONFIG_SECRET_DEBUG_FILE).read())

DEBUG = True
ALLOWED_HOSTS = config_secret_debug['django']['allowed_hosts']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS.append('django_extensions')

WSGI_APPLICATION = 'config.wsgi.debug.application'


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
MEDIA_URL='/media/'

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
