"""
Django settings for liwi project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '69)jz9t9^kvci2_8^j732h%a*8yz4h-(kehld1@e2jcw_d9wkn'

AWS_ACCESS_KEY_ID = 'AKIAJEYC7OVXICWHIFMA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_SES_REGION_NAME = 'us-west-2'
AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'


#s3 config
AWS_S3_SECURE_URLS = False       # use http instead of https
AWS_QUERYSTRING_AUTH = False     # don't add complex authentication-related query parameters for requests
AWS_S3_ACCESS_KEY_ID = 'AKIAJEYC7OVXICWHIFMA'
AWS_S3_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'liwi'

TESTING = 'test' in sys.argv

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'south',
    'registration',
    'authentication',
    'home',
    'user_profile',
    'art',
    'artists',
    'cart',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
)

ROOT_URLCONF = 'liwi.urls'

WSGI_APPLICATION = 'liwi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'liwi',
        'USER': 'kshafer',
        'PASSWORD': 'Rubygem14',
        'HOST': 'liwi.c2mw5t19dwbx.us-west-2.rds.amazonaws.com',
        'PORT': '5432',
    },
    'liwi_test': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'liwi_test',
        'USER': 'kshafer',
        'PASSWORD': 'Rubygem14',
        'HOST': 'liwi.c2mw5t19dwbx.us-west-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

AUTH_USER_MODEL = 'registration.User'

LOGIN_URL = '/login'

SITE_ROOT = '/home/ubuntu/liwi-site'

if TESTING:
    MEDIA_ROOT = '/home/ubuntu/liwi-site/test_photos/'
    MEDIA_URL = '/test_photos/'
else:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'


#if testing, send messages with a file based backend
#NOTE: the run_tests script will create and tear down the mail directory
if TESTING:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = 'mail/' 
else:
    EMAIL_BACKEND = 'django_ses.SESBackend'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': SITE_ROOT + "/logfile.txt",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'liwi': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}
