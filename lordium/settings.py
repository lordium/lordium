"""
Django settings for lordium project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from datetime import timedelta
import os
import logging
import sys

#for celery
import djcelery
djcelery.setup_loader()
BROKER_URL = 'django://'


ENVIRONMENT = os.getenv("LORDIUM_ENVIRONMENT")

development = False

if ENVIRONMENT == "dev" or ENVIRONMENT == "DEV":
    development = True
    LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}

    if len(sys.argv) > 1:
        level_name = sys.argv[1]
        level = LEVELS.get(level_name, logging.NOTSET)
        logging.basicConfig(level=level)
    logging.info("Development Mode")
else:
    database_name = os.getenv("LORDIUM_DATABASE_NAME")
    database_user = os.getenv("LORDIUM_DATABASE_USER")
    database_password = os.getenv("LORDIUM_DATABASE_PASSWORD")


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from os.path import join
TEMPLATE_DIRS = (
    join(BASE_DIR,  'templates'),
    join(BASE_DIR,  'app/static'),
)


STATIC_ROOT = join(BASE_DIR,  'super_static')



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^#3&wa7m43_4d6te-y2on-x4u=__w*d_e)iptq_d*t#bg&59(@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = development

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'darbaan',
    'djcelery',
    'kombu.transport.django',
    'tasker'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'

)

# Authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'lordium.urls'

WSGI_APPLICATION = 'lordium.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if development:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
           'NAME': database_name,                      # Or path to database file if using sqlite3.
           # The following settings are not used with sqlite3:
           'USER': database_user,
           'PASSWORD': database_password,
           'HOST': 'localhost',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
           'PORT': '',                      # Set to empty string for default.
       }
   }


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = None

# if DEBUG == True:
#     STATICFILES_DIRS = (
#         os.path.join(BASE_DIR, "app/static"),
#         # '/var/www/static/',
#     )
# else:
STATICFILES_DIRS =(
    os.path.join(BASE_DIR, "app/static/dist/static"),

)

POSTS_PER_REQUEST = 5

CELERY_IMPORTS = ("app.tasks",)

CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'app.tasks.fetch_posts',
        'schedule': timedelta(seconds=30),
        'args': (16, 16)
    },
}

