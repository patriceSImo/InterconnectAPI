from pathlib import Path
import os
from dotenv import load_dotenv
import environ
from colorlog import ColoredFormatter

# Définir le répertoire de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = os.path.join(BASE_DIR, 'logs')


# Applications installées
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

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wifirstAPI.middlewares.saveReqmiddlewares.ReqStatsMiddleware',
    'wifirstAPI.middlewares.middlewares.APICallLoggingMiddleware',
    'wifirstAPI.middlewares.middlewares.APITokenMiddleware',
]

# Configuration de l'URL principale
ROOT_URLCONF = 'cometeAPIs.urls'

# Configuration des templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# Application WSGI
WSGI_APPLICATION = 'cometeAPIs.wsgi.application'

# Configuration des routeurs de base de données
DATABASE_ROUTERS = ['cometeAPIs.db_routers.MultiDBRouter']



# Configuration des bases de données

# Lire le fichier .env s'il existe
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

env = environ.Env(
    # Définir les variables par défaut
    DEBUG=(bool, False)
)
load_dotenv()


DATABASES = {
    "default": {'ENGINE': env('DB_ENGINE_3'),
        'NAME': env('DB_NAME_3'),
        'USER': env('DB_USER_3'),
        'PASSWORD': env('DB_PASSWORD_3'),
        'HOST': env('DB_HOST_3'),
        'PORT': env('DB_PORT_3'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES';",
},
   },
    
    env('DB_CALL_NAME_1'): {
        'ENGINE': env('DB_ENGINE_1'),
        'NAME': env('DB_NAME_1'),
        'USER': env('DB_USER_1'),
        'PASSWORD': env('DB_PASSWORD_1'),
        'HOST': env('DB_HOST_1'),
        'PORT': env('DB_PORT_1'),
         'OPTIONS': {
            'charset': 'utf8',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES';",
        },
    },
    env('DB_CALL_NAME_3'): {
        'ENGINE': env('DB_ENGINE_3'),
        'NAME': env('DB_NAME_3'),
        'USER': env('DB_USER_3'),
        'PASSWORD': env('DB_PASSWORD_3'),
        'HOST': env('DB_HOST_3'),
        'PORT': env('DB_PORT_3'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES';",
},
    },
    
    
}


# Clé secrète (Assurez-vous de la garder secrète en production)
SECRET_KEY = env('SECRET_KEY', default='django-insecure-8%dff8zsw9$ao*!gb7howk#nhu_7a3fzh920zj8@axx09&hzk@')

# Définir le mode débogage (à désactiver en production)
DEBUG = env('DEBUG')

# Définir les hôtes autorisés
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['172.18.0.2','api-prod.comete.ai','127.0.0.1', 'localhost','185.97.144.32'])



# Validation des mots de passe
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

# Configuration de la langue et du fuseau horaire
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Configuration des fichiers statiques
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Configuration du champ auto par défaut
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration de REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'EXCEPTION_HANDLER': 'wifirstAPI.utils.custom_exception_handler',
}

# Configuration de JWT
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
}

# Configuration des backend d'authentification
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# URL de redirection après login/logout
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/login/'

# Configuration des logs (exemple)
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
            '()': 'colorlog.ColoredFormatter',
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
            'filename': os.path.join(LOG_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'wifirstAPI': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
