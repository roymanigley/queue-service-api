import os
import logging
import l4py
from pathlib import Path
from dotenv import load_dotenv
import tempfile

load_dotenv('.django.env')

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = os.environ.get('DJANGO_DB_DIR', BASE_DIR)

SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-i7d_4&2#m!ih$klw*sqfbl35_rwa3xdv76$5-0no%#)2fv4w(u'
)

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = os.getenv(
    'DJANGO_ALLOWED_HOSTS', '*'
).split(' ')

CSRF_TRUSTED_ORIGINS = os.getenv(
    'DJANGO_TRUSTED_ORIGINS', 'http://localhost:8000 http://127.0.0.1:8000'
).split(' ')

# Application definition
DEBUG = os.environ.get('DJANGO_DEBUG').lower() == 'true'


INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_spectacular',
    'oauth2_provider',
    'rest_framework',
    'apps.authentication',
    'apps.core',
    'apps.shared',
]

AUTH_USER_MODEL = "authentication.UserProfile"

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGOUT_URL = '/api/auth/logout/'
LOGIN_URL = '/api/auth/login/'
LOGIN_REDIRECT_URL = '/auth/accounts/'
LOGOUT_REDIRECT_URL = '/'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ]
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Customer Queue',
    'DESCRIPTION': f'''
--- 
**Login:** [POST] [{LOGIN_URL}]({LOGIN_URL})  
**Logout:** [POST] [{LOGOUT_URL}]({LOGOUT_URL})
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'config.middlewares.ThreadLocalMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DB_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = f'/{tempfile.gettempdir()}/static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = l4py.LogConfigBuilderDjango()\
    .django_log_level(logging.INFO)\
    .add_logger('apps', logging.INFO)\
    .add_logger('config', logging.INFO)\
    .file_enabled(False)\
    .build_config()

JAZZMIN_SETTINGS = {
    "site_title": "Customer Queue",
    "site_header": "Customer Queue",
    "site_brand": "Customer Queue",
    "welcome_sign": "Welcome to Customer Queue",
}
