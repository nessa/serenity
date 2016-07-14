from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xl)b4y_2(!9)%rz31tdk7)^@gbjm6z96qpw^0z!n^tdv$ewc66'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}
