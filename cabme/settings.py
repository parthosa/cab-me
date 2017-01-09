"""
Django settings for cabme project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
from email_config import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's1no3l6mxm=rasgm*8y+02s6uere(+3djy*!u21qga(#al(h5^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', 'cabme.in']

SITE_ID = 1
# Application definition

TEMPPLATE_CONTEXT_PROCESSORS = (
    'django.template.context_processors.request',
    "django.contrib.auth.context_processors.auth",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'registration',
    'cab',
    'b_cab',
    'vendor',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
)

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

)

ROOT_URLCONF = 'cabme.urls'

WSGI_APPLICATION = 'cabme.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

STATIC_ROOT = 'static'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
# ACCOUNT_SIGNUP_FORM_CLASS = 'registration.forms.SocialForm'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/registration/contact'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email'],
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'METHOD': 'js_sdk'  # instead of 'oauth2'
    }
}
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

from django.core.mail.backends.smtp import EmailBackend


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = config.email_host
# EMAIL_HOST_USER = config.email_host_user
# EMAIL_HOST_PASSWORD = config.email_host_pass
# EMAIL_PORT = config.email_port
# EMAIL_USE_TLS = True

#change settings