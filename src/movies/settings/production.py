import dj_database_url
from .base import *

DEBUG = False

DATABASES = {
    'default': dj_database_url.config()
}

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS.append('https://collectmovies.herokuapp.com/')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
