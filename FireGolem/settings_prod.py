from settings import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DEBUG = False

# Logging

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'FireGolem',
        'USER': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
