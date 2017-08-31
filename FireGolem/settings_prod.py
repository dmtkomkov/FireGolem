from settings import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DEBUG = False

STATIC_ROOT = '/var/www/FireGolem/static/'

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