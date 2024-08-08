"""
Paramètres Django pour le projet cometeAPIs.

Généré par 'django-admin startproject' utilisant Django 5.0.7.

Pour plus d'informations sur ce fichier, consultez
https://docs.djangoproject.com/en/5.0/topics/settings/

Pour la liste complète des paramètres et leurs valeurs, consultez
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Construire des chemins à l'intérieur du projet comme ceci : BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Paramètres de démarrage rapide pour le développement - ne convient pas à la production
# Voir https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# ATTENTION : gardez la clé secrète utilisée en production secrète !
SECRET_KEY = 'django-insecure-8%dff8zsw9$ao*!gb7howk#nhu_7a3fzh920zj8@axx09&hzk@'

# ATTENTION : ne pas exécuter avec le débogage activé en production !
DEBUG = False

ALLOWED_HOSTS = ['api-preprod.comete.ai', '185.97.144.32']

import os
from pathlib import Path
from colorlog import ColoredFormatter

BASE_DIR = Path(__file__).resolve().parent.parent

ENABLE_CONSOLE_LOG = os.getenv('ENABLE_CONSOLE_LOG', 'False') == 'True'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'colored': {
            '()': ColoredFormatter,
            'format': '%(log_color)s%(levelname)s:%(name)s:%(message)s',
            'log_colors': {
                'DEBUG': 'bold_black',
                'INFO': 'bold_green',
                'WARNING': 'bold_yellow',
                'ERROR': 'bold_red',
                'CRITICAL': 'bold_purple',
            },
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'wifirstAPI': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

if ENABLE_CONSOLE_LOG:
    LOGGING['handlers']['console'] = {
        'level': 'DEBUG',
        'class': 'logging.StreamHandler',
        'formatter': 'colored',
    }
    LOGGING['loggers']['django']['handlers'].append('console')
    LOGGING['loggers']['wifirstAPI']['handlers'].append('console')

# Définition de l'application

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'wifirstAPI',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wifirstAPI.middlewares.middlewares.APICallLoggingMiddleware',
    'wifirstAPI.middlewares.middlewares.APITokenMiddleware',
]


ROOT_URLCONF = 'cometeAPIs.urls'

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

WSGI_APPLICATION = 'cometeAPIs.wsgi.application'

# Base de données
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validation des mots de passe
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Internationalisation
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Fichiers statiques (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
#STATIC_ROOT = BASE_DIR / 'static'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Type de champ de clé primaire par défaut
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.permissions.IsAuthenticated',
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
}

