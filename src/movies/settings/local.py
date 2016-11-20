from .base import *

SECRET_KEY = '+2f_2khp#yx+r-ntq*o4k&25j^i0@$ah4djy6mao79478x493j'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'database\db.sqlite3'),
    }
}
