import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'notsecret'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test.db'),
    }
}

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'rest_framework',
    'representatives',
    'representatives_votes',
)

DEBUG = True
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
ROOT_URLCONF = 'representatives_votes.tests.urls'

STATIC_URL = '/static/'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s[%(module)s]: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'representatives': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'representatives_votes': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
    },
}
