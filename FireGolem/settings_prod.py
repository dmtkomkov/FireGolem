from settings import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'firegolem.perforator.xyz']

# Allow frontend access
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ['stormgolem.perforator.xyz']

DEBUG = False

# Logging

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'FireGolem',
        'USER': 'user',
        'PASSWORD': 'user',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

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
