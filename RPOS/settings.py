"""
Django settings for RPOS project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q3!v&-(ii$@@m74$f8zr^_9qzdxs(-$+=ycr(e==$cvmudp2=!'

AUTHENTICATION_BACKENDS = (
    # 'social_core.backends.google.GoogleOAuth2',
        'django.contrib.auth.backends.ModelBackend',

)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
from django.core.servers.basehttp import WSGIServer
WSGIServer.handle_error = lambda *args, **kwargs: None

ALLOWED_HOSTS=['*']


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", 
]


# Application definition

INSTALLED_APPS = [
    'Stores',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',

]

# PASSWORD_HASHERS = [
#     'django.contrib.auth.hashers.Argon2PasswordHasher',
#     'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
#     'django.contrib.auth.hashers.BCryptPasswordHasher',
#     'django.contrib.auth.hashers.PBKDF2PasswordHasher',
# ]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.multipart.MultiPartMiddleware',

]

ROOT_URLCONF = 'RPOS.urls'

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

WSGI_APPLICATION = 'RPOS.wsgi.application'

REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES': (
       
        # 'rest_framework_simplejwt.authentication.JWTAuthentication', 
    #      'rest_framework.authentication.BasicAuthentication',
    #    'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',

   ),
   'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.IsAuthenticated',
), }

# PASSWORD_HASHERS = [
#     "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
#     "django.contrib.auth.hashers.PBKDF2PasswordHasher",
#     "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
#     "django.contrib.auth.hashers.Argon2PasswordHasher",
#     "django.contrib.auth.hashers.ScryptPasswordHasher",
# ]


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'einvoicing3',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#         'USER': 'root',
#         'PASSWORD':'7379585Eman4444@',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'einvoicing3',
#         'HOST': '192.168.1.16',
#         'PORT': '3306',
#         'USER': 'root',
#         'PASSWORD':'123',
#     }
# }
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
# AUTH_USER_MODEL = "User.User"

CSRF_TRUSTED_ORIGINS = ['http://localhost:3000']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True


CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]


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




LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
from django.core.mail import send_mail



STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# SIMPLE_JWT = {
#     "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
#     'USER_ID_FIELD': 'UserID',
#     "ACCESS_TOKEN_LIFETIME" : timedelta(days=1),
# }

DB_Email = 'adhamhelbawy01@gmail.com'
DB_Pass = 'mmlolmeodngdldxh'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = DB_Email
EMAIL_HOST_PASSWORD = DB_Pass

import os

# if os.getcwd() == '/User':
#     DEBUG = False
