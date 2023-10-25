from datetime import timedelta
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-%ata-o!nrmt6jnaa1b4nvaqmhu#s1qbenwx=(p64x^a)20#s5o'

API_VERSION = "v1"

APPEND_SLASH = False

DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'Domain',
    'Domain.category',
    'Domain.account',
    'Domain.auth',
    'Domain.phone',
    'Domain.reduction',
    'Domain.follower',
    'Domain.password',
    'Domain.conversation',
    'Domain.additionalInfo',
    'Domain.notification',
    'Domain.message',
    'Domain.product',
    'Domain.brand',
    'Domain.offer',
    'Domain.order',
    'Domain.deliverySetting',
    'Domain.paiementMethod',
    'Domain.review',
    'Domain.report',
    'Domain.wallet',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'second_chance_api.urls'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect'
            ],
        },
    },
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "TOKEN_OBTAIN_SERIALIZER": "Domain.auth.serializers.LoginSerializer",
}

AUTH_USER_MODEL = 'Domain_account.User'

WSGI_APPLICATION = 'second_chance_api.wsgi.application'
ASGI_APPLICATION = "second_chance_api.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.environ.get("REDIS_HOST"), os.environ.get("REDIS_PORT"))],
        },
    },
}

REST_FRAMEWORK = {

    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

    'DEFAULT_AUTHENTICATION_CLASSES':
        [
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ],
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}

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

STATIC_URL = 'assets/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# for CELERY
CELERY_BROKER = 'redis://redis:6379/0'
CELERY_BACKEND = 'redis://redis:6379/1'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# For MAILS
SENDGRID_API_KEY = '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'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Facebook configuration
SOCIAL_AUTH_FACEBOOK_KEY = '636862301499510'
SOCIAL_AUTH_FACEBOOK_SECRET = 'a9c91ab1516b100a46118970226e3813'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'fields': 'id, name, email, gender'}



# Google configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '878013306916-sp0q16r0njb9bv9963rlhqfompmccjif.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

# Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]
