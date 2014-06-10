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

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
    'registration',
    'authentication',
    'home',
    'user_profile',
    'art',
    'artists',
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
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
    'liwi_test': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'liwi',
        'USER': 'kshafer',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
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

if TESTING:
    MEDIA_ROOT = '/Users/kshafer/workspace/Django/liwi/test_photos/'
    MEDIA_URL = '/test_photos/'
else:
    MEDIA_ROOT = '/Users/kshafer/workspace/Django/liwi/photos/'
    MEDIA_URL = '/photos/'

#if testing, send messages with a file based backend
#NOTE: the run_tests script will create and tear down the mail directory
if TESTING:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = 'mail/' 
else:
    EMAIL_HOST = 'mailtrap.io'
    EMAIL_HOST_USER = '21083908bd7b8551c'
    EMAIL_HOST_PASSWORD = 'f0bc9572503d2b'
    EMAIL_PORT = '2525'
    EMAIL_USE_TLS = True