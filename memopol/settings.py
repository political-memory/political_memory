"""
Django settings for memopol project.

Uses the following environment variables:
- DJANGO_DEBUG: set to "true" to enable debugging (default false)
- DJANGO_LANGUAGE_CODE: language (default en-us)
- DJANGO_LOG_LEVEL: log leve (defaults to INFO or DEBUG if debug enabled)
- DJANGO_ALLOWED_HOSTS: comma-separated additional allowed hosts (default none)
"""

import os
from socket import gethostname

from django.conf import global_settings
from django.utils.crypto import get_random_string


###############################################################################
#
# Base memopol settings
#

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = os.environ.get('DJANGO_DEBUG', 'false').lower() == 'true'

#
# Main Django config
#

ROOT_URLCONF = 'memopol.urls'
WSGI_APPLICATION = 'memopol.wsgi.application'

#
# Apps
#

INSTALLED_APPS = (
    'dal',
    'dal_select2',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',

    # 3rd party apps
    'compressor',
    'bootstrap3',
    'datetimewidget',
    'django_filters',
    'fontawesome',
    'rest_framework',
    'taggit',

    # memopol apps
    'core',
    'memopol',
    'memopol_scores',
    'memopol_settings',
    'memopol_themes',
    'representatives',
    'representatives_votes',
    'representatives_recommendations',
    'representatives_positions',
)

if DEBUG:
    try:
        import debug_toolbar  # noqa
    except:
        pass
    else:
        INSTALLED_APPS += ('debug_toolbar',)

    try:
        import django_extensions  # noqa
    except:
        pass
    else:
        INSTALLED_APPS += ('django_extensions',)


#
# Middleware
#

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
)

#
# Sessions
#

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

#
# Internationalization
#

LANGUAGE_CODE = os.environ.get('DJANGO_LANGUAGE_CODE', 'en-us')
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#
# Templating
#

TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.template.context_processors.request',
    'memopol.context_processors.search_form_options',
)

#
# Cache
#

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

#
# Static files and related settings
#

STATIC_URL = '/static/collected/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MEDIA_URL = '/static/media/'

COMPRESS_ENABLED = False

#
# Logging
#

LOG_LEVEL = os.environ.get('DJANGO_LOG_LEVEL', 'DEBUG' if DEBUG else 'INFO')

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
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'memopol': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        },
        'representatives': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        },
        'representatives_positions': {
            'handlers': ['console'],
            'level': LOG_LEVEL
        },
        'representatives_recommendations': {
            'handlers': ['console'],
            'level': LOG_LEVEL
        },
        'representatives_votes': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        }
    },
}

###############################################################################
#
# Local settings
#

#
# Defaults
#

DATA_DIR = 'data'
LOG_DIR = 'log'
PUBLIC_DIR = 'wsgi/static'


DATABASES = {
    'default': {
        'NAME': 'memopol',
        'USER': 'memopol',
        'PASSWORD': 'memopol',
        'HOST': 'localhost',
        'PORT': '5432',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
    }
}


ALLOWED_HOSTS = [
    gethostname(),
]


SITE_ID = 1
SITE_NAME = 'Memopol'
SITE_DOMAIN = gethostname()

ORGANIZATION_NAME = 'Memopol'

#
# Import local overrides
#

try:
    from local_settings import *  # noqa
except ImportError:
    pass

#
# Local directories
#

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
COMPRESS_ROOT = os.path.join(DATA_DIR, 'compress')
STATIC_ROOT = os.path.join(PUBLIC_DIR, 'collected')

if DEBUG:
    LOGGING['handlers']['debug'] = {
        'level': 'DEBUG',
        'class': 'logging.FileHandler',
        'filename': os.path.join(LOG_DIR, 'debug.log'),
    }

    for logger in LOGGING['loggers'].values():
        logger['handlers'].append('debug')

#
# Secret file
#

SECRET_FILE = os.path.join(DATA_DIR, 'secret.txt')

if not os.path.exists(SECRET_FILE):
    # Create random secret on first execution
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    with open(SECRET_FILE, 'w+') as f:
        f.write(get_random_string(50, chars))

with open(SECRET_FILE, 'r') as f:
    SECRET_KEY = f.read()

#
# Add allowed hosts from environment
#

if 'DJANGO_ALLOWED_HOSTS' in os.environ:
    ALLOWED_HOSTS += os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')

#
# Raven configuration
#
# Put a 'sentry' file with Sentry DSN in DATA_DIR to enable.
# Optionally, put an empty 'sentry.404' in DATA_DIR to log 404s.
#

RAVEN_FILE = os.path.join(DATA_DIR, 'sentry')
RAVEN_404_FILE = os.path.join(DATA_DIR, 'sentry.404')

if os.path.exists(RAVEN_FILE):
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)

    LOGGING['handlers']['sentry'] = {
        'level': 'INFO',
        'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
    }
    LOGGING['loggers']['sentry.errors'] = LOGGING['loggers']['raven'] = {
        'level': 'INFO',
        'handlers': ['console'],
        'propagate': False,
    }

    if os.path.exists(RAVEN_404_FILE):
        RAVEN_MIDDLEWARE = (
            'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',  # noqa
        )

        MIDDLEWARE_CLASSES = RAVEN_MIDDLEWARE + MIDDLEWARE_CLASSES

    with open(RAVEN_FILE, 'r') as f:
        RAVEN_CONFIG = {'dsn': f.read().strip()}
