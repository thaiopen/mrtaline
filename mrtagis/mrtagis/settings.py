"""
Django settings for mrtagis project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from email_info import *
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8r=%w)%%pwyz$gsq#lfx(qg=ts=n3k-29l^=pq3abw5@00^a9w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
    'django.contrib.gis',
    'uuslug',
    'crispy_forms',
    'fsm_admin',
    'uuidfield',
    'leaflet',
    'bootstrap3',
    'djgeojson',
    'home',
    'reports',
    'tasks',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mrtagis.urls'

WSGI_APPLICATION = 'mrtagis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mrtagis_development',
        'USER': 'admin',
        'PASSWORD': 'bangkok',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'Asia/bangkok'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
APPEND_SLASH = True


TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR),"static","templates"),
)

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
MEDIA_ROOT =  os.path.join(os.path.dirname(BASE_DIR),"static","media")
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR),"static","static-only")
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR),"static","static"),
)


LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (13.736717,100.523186 ),
    'DEFAULT_ZOOM': 12,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 24,
}

from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)


CRISPY_TEMPLATE_PACK = 'bootstrap3'


#mark for git