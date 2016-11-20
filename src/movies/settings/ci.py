from .base import *
import random
import string


DEBUG = False
SECRET_KEY = ''.join(
    [
        random.SystemRandom().choice("{}{}{}".format(
            string.ascii_letters,
            string.digits,
            string.punctuation)
        ) for i in range(50)
    ]
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'database/db.sqlite3'),
    }
}
