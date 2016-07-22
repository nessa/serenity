from .base import *
from configparser import RawConfigParser

# External configuration
config = RawConfigParser()
config.read('/etc/serenity-settings.ini')

# Host setting
ALLOWED_HOSTS = ['amuse-bouche.noeliarcado.es']

# Disable debug
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('secret', 'SECRET_KEY')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # Include the default Django email handler for errors
        # This is what you'd get without configuring logging at all.
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
             # But the emails are plain text by default - HTML is nicer
            'include_html': True,
        },
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/django/serenity.log'
        },
    },
    'loggers': {
        # Might as well log any errors anywhere else in Django
        'django': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': True,
        },
        # Your own app - this assumes all your logger names start with "recipes".
        'recipes': {
            'handlers': ['logfile'],
            'level': 'WARNING', # Or maybe INFO or DEBUG
            'propagate': True
        },
    },
}


# Postgre database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config.get('database', 'DATABASE_NAME'),
        'USER': config.get('database', 'DATABASE_USER'),
        'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
        'HOST': '127.0.0.1'
    }
}
