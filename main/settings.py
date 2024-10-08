"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import sys
import os
import dj_database_url
from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key

load_dotenv(override=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())
                            

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'djstripe',
    'phonenumber_field',
    'django_recaptcha',
    'storages',

    'main',
    'users',
    'accounts',
    'pcr',
    'store',
    'guide',
    'analytics',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'main.middleware.custom.TimezoneMiddleware'
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if DEVELOPMENT_MODE is True:
  DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
  }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
  if os.getenv("DATABASE_URL", None) is None:
    raise Exception("DATABASE_URL environment variable not defined")
  DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
  }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# LOCAL SETTINGS
# STATIC_URL = "/static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# PRODUCTION SETTINGS
STATIC_URL = "/static/"

STATICFILES_DIRS = [
  BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles-cdn"

from .cdn.conf import * # noqa


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


# Custom settings
handler404 = 'accounts.views.custom_404'
handler500 = 'accounts.views.custom_500'
handler403 = 'accounts.views.custom_403'

# Custom user extension
AUTH_USER_MODEL = 'users.User'
SESSION_COOKIE_AGE = 43200 # 12 Hours
SESSION_SAVE_EVERY_REQUEST = True # Save session cookie for every successful request by user

#Google reCAPTCHA settings
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')

# Settings for account activation via email
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_FROM = config('EMAIL_FROM')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_ALIAS = os.getenv('EMAIL_ALIAS')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
PASSWORD_RESET_TIMEOUT = 14400

# Stripe
STRIPE_LIVE_SECRET_KEY = os.getenv('STRIPE_LIVE_SECRET_KEY')
STRIPE_TEST_SECRET_KEY = os.getenv('STRIPE_TEST_SECRET_KEY')
STRIPE_LIVE_MODE = os.getenv('STRIPE_LIVE_MODE', "False") == "True" # Change to True in production
DJSTRIPE_WEBHOOK_SECRET = os.getenv('DJSTRIPE_WEBHOOK_SECRET') # Get it from the section in the Stripe dashboard where you added the webhook endpoint
DJSTRIPE_USE_NATIVE_JSONFIELD = True  # We recommend setting to True for new installations
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"

# MillionVerifier
MILLION_VERIFIER_KEY = os.getenv('MILLION_VERIFIER_KEY')

# Google Oauth
GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID')

# Referrer policy
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"