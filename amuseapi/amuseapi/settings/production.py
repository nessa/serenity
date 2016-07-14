from .base import *
from configparser import RawConfigParser

# External configuration
config = RawConfigParser()
config.read('/etc/serenity-settings.ini')

# Host setting
HOST = os.environ.get('HOST', 'http://localhost')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('secret', 'SECRET_KEY')

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config.get('database', 'DATABASE_NAME'),
        'USER': config.get('database', 'DATABASE_USER'),
        'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
        'HOST': '127.0.0.1'
    }
}
