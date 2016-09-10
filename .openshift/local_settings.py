"""
Memopol local settings for Openshift.
"""

import os


DATA_DIR = os.environ['OPENSHIFT_DATA_DIR']
LOG_DIR = os.environ['OPENSHIFT_LOG_DIR']
PUBLIC_DIR = os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi/static')


DATABASES = {
    'default': {
        'NAME': os.environ['OPENSHIFT_APP_NAME'],
        'USER': os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
        'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
        'HOST': os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
        'PORT': os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
    }
}


ALLOWED_HOSTS = [
    os.environ['OPENSHIFT_APP_DNS'],
]


SITE_ID = 1
SITE_NAME = 'Memopol'
SITE_DOMAIN = os.environ['OPENSHIFT_APP_DNS']

ORGANIZATION_NAME = 'Memopol'
