import os
import sys
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost').split()
CSRF_TRUSTED_ORIGINS = os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').split()


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cachalot',
    'rest_framework',
    'drf_spectacular',
    'adminsortable2',
    'django_ckeditor_5',
    'django_cleanup.apps.CleanupConfig',
    'diskette',
    'dj_cache_panel',
    'homepage.apps.HomepageConfig',
    'cars.apps.CarsConfig',
    'api.apps.ApiConfig',
    'contacts.apps.ContactsConfig',
    'dragndrop_related',
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

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
    INSTALLED_APPS = [
        *INSTALLED_APPS,
        'debug_toolbar',
    ]
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        *MIDDLEWARE,
    ]
    INTERNAL_IPS = [
        '127.0.0.1',
        'localhost',
    ]
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.history.HistoryPanel',
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'cachalot.panels.CachalotPanel',
    ]
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_COLLAPSED': False,
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': os.environ.get('REDIS_URL', 'redis://redis:6379/0'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'KEY_PREFIX': 'sochnoauto',
        }
    }

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'homepage/templates',
            BASE_DIR / 'cars/templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.current_year',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': os.environ.get(
            'DJANGO_DB_ENGINE', 'django.db.backends.sqlite3'
        ),
        'NAME': os.environ.get('POSTGRES_DB', str(BASE_DIR / 'db.sqlite3')),
        'USER': os.environ.get('POSTGRES_USER', ''),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('DJANGO_DB_HOST', 'localhost'),
        'PORT': os.environ.get('DJANGO_DB_PORT', ''),
    }
}


# Password validation

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


# REST Framework

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


# API Documentation

SPECTACULAR_SETTINGS = {
    'TITLE': 'SochnoAuto API',
    'DESCRIPTION': 'API для автосалона SochnoAuto',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}


# Caching (django-cachalot)
# Настройки времени кэширования в core/cache.py

from core.cache import (CACHE_CAR_DETAIL, CACHE_CATEGORIES,
                        CACHE_CATEGORY_CARS, CACHE_FEEDBACKS,
                        CACHE_SPECIAL_OFFERS)

CACHALOT_ENABLED = not DEBUG
CACHALOT_TIMEOUT = CACHE_CATEGORY_CARS

CACHALOT_MODEL_PRESET_TIMEOUTS = {
    'homepage.Feedback': CACHE_FEEDBACKS,
    'homepage.HomepageImage': CACHE_SPECIAL_OFFERS,
    'cars.Car': CACHE_CAR_DETAIL,
    'cars.CarImage': CACHE_CAR_DETAIL,
    'cars.CarParameter': CACHE_CAR_DETAIL,
    'cars.CarCategory': CACHE_CATEGORIES,
}

if 'test' in sys.argv:
    CACHALOT_ENABLED = False
    CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'


# Internationalization

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

AVITO_SELLER_ID = os.environ.get('AVITO_SELLER_ID')
AVITO_BRAND_ID = os.environ.get('AVITO_BRAND_ID')

# Logging

LOGS_DIR = BASE_DIR / 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': {
            'items': [
                'heading', '|', 'bold', 'italic', 'underline', 'link',
                '|', 'fontSize', 'fontFamily', 'fontColor', 'alignment', '|',
                'bulletedList', 'numberedList', 'blockQuote', 'insertTable',
            ],
        },
        'language': 'ru',

    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / "django_info.log",
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'errors_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / "django_errors.log",
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'homepage': {
            'handlers': ['console', 'file', 'errors_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'cars': {
            'handlers': ['console', 'file', 'errors_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'api': {
            'handlers': ['console', 'file', 'errors_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'contacts': {
            'handlers': ['console', 'file', 'errors_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

if 'test' in sys.argv or 'pytest' in sys.argv:
    LOGGING['handlers']['console']['level'] = 'CRITICAL'
    LOGGING['handlers']['file']['level'] = 'CRITICAL'
    LOGGING['handlers']['errors_file']['level'] = 'CRITICAL'
    LOGGING['loggers']['django.db.backends']['level'] = 'CRITICAL'

# EMAIL BACKEND

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS') == 'True'
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL') == 'True'
EMAIL_TIMEOUT = os.environ.get('EMAIL_TIMEOUT')
EMAIL_FOR = os.environ.get('EMAIL_FOR').split()

# DISKETTE
DISKETTE_APPS = [
    ('cars', {
        'comments': 'cars: Изображения, категории, параметры и автомобили',
        'natural_foreign': True,
        'models': [
            'cars.Car', 'cars.CarCategory',
            'cars.CarImage', 'cars.CarParameter'
        ]
    }),
    ('homepage', {
        'comments': 'homepage: Отзывы и изображения',
        'models': ['homepage.Feedback', 'homepage.HomepageImage']
    }),
    ('contacts', {
        'comments': 'contacts: Заявки',
        'models': ['contacts.RequestContact']
    }),
]
DISKETTE_ADMIN_ENABLED = False
DISKETTE_DUMP_PATH = BASE_DIR / 'dumps'
DISKETTE_DUMP_FILENAME = 'dump.tar.gz'
DISKETTE_DUMP_PERMISSIONS = 0o755
DISKETTE_DOWNLOAD_ALLOWED_PROTOCOLS = ('http://', 'https://')
DISKETTE_LOAD_STORAGES_PATH = BASE_DIR
DISKETTE_LOAD_MINIMAL_FILESIZE = 6
DISKETTE_STORAGES = [MEDIA_ROOT]
DISKETTE_STORAGES_EXCLUDES = [
    'cache/*',
    'pil/*',
    'public/thumbnails/*',
]

# ADDITIONAL SETTINGS

LIFETIME_TOKEN_CONTACTS = timedelta(minutes=10)
