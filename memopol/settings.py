"""
Django settings for memopol project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import json
import os
import django

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

with open(config_file) as f:
    config = json.loads(f.read())


def get_param(setting, config=config, default=None):
    """Get the secret variable or return explicit exception."""
    try:
        return config[setting]
    except KeyError:
        if default:
            return default
        error_msg = "Set the {0} config variable".format(setting)
        raise ImproperlyConfigured(error_msg)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_param('secret_key')

DEBUG = get_param('debug')
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

COMPOTISTA_SERVER = get_param('compotista_server')
TOUTATIS_SERVER = get_param('toutatis_server')
REDIS_DB = get_param('redis_db')

# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    'django.contrib.admin.apps.SimpleAdminConfig',  # Instead of contrib.admin to use Django-Admin-Plus
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ---
    'compressor',
    # 'chronograph',
    'adminplus',
    # ---
    'core',
    'representatives',
    'representatives_votes',
    'legislature',
    'votes',
)


if DEBUG:
    INSTALLED_APPS += tuple(get_param('dev_modules'))


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'memopol.urls'

WSGI_APPLICATION = 'memopol.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': get_param('database_name'),
        'USER': get_param('database_user'),
        'PASSWORD': get_param('database_password'),
        'HOST': get_param('database_host'),
        'PORT': get_param('database_port'),
    }
}

if get_param('database_server') == 'mysql':
    DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
elif get_param('database_server') == 'postgresql':
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = get_param('language_code', default='en-us')

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# HAML Templates
# https://github.com/jessemiller/hamlpy

TEMPLATE_DIRS = (
    'core/templates',
    os.path.dirname(django.__file__)
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'hamlpy.template.loaders.HamlPyFilesystemLoader',
    'hamlpy.template.loaders.HamlPyAppDirectoriesLoader',
)

"""
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'hamlpy.template.loaders.HamlPyFilesystemLoader',
        'hamlpy.template.loaders.HamlPyAppDirectoriesLoader',
    )),
)
"""

# Static files finders

STATIC_URL = '/static/'
COMPRESS_ROOT = 'static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    # ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-sass', 'sass {infile} {outfile}'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
    # ('text/stylus', 'stylus < {infile} > {outfile}'),
    # ('text/foobar', 'path.to.MyPrecompilerFilter'),
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s[%(module)s]: %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/compotista-debug.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'memopol': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'representatives': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'representatives_votes': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    },
}
