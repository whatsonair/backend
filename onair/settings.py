from configurations import Configuration, values

import os


class Settings(Configuration):
    ALLOWED_HOSTS = values.ListValue(['*'])
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
    AUTH_USER_MODEL = 'telegrambot.User'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CACHES = values.CacheURLValue('locmem://')
    DATABASES = values.DatabaseURLValue('sqlite:///db.sqlite3')
    # DOTENV = os.path.join(BASE_DIR, '.env')
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(True)
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # third party
        'rest_framework',
        # local apps
        'telegrambot',
    ]
    LANGUAGE_CODE = 'en-us'
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "command_notify": {
                "level": "DEBUG",
                "handlers": ['console'],
                "propagate": False
            },
            "scrappers": {
                "level": "DEBUG",
                "handlers": ['console'],
                "propagate": False
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple"
            }
        },
        "formatters": {
            "simple": {
                "format": "%(asctime)s [%(levelname)s] {%(module)s} %(message)s"
            }
        }
    }
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    PREVENT_NOTIFICATION_REPEAT_TIMEOUT = values.PositiveIntegerValue(5 * 60)  # 5 mins
    ROOT_URLCONF = 'onair.urls'
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 10,
        'URL_FIELD_NAME': 'href',
    }
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '1)#=9)t+e=374nx2i*p-o$a_b7%zvreb1ghmxo21+iyh&_*+a9'
    STATIC_ROOT = values.Value(os.path.join(BASE_DIR, '..', 'staticfiles'))
    STATIC_URL = '/assets/'
    # http://whitenoise.evans.io/en/stable/
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    TELEGRAM_TOKEN = values.SecretValue()
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
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    WSGI_APPLICATION = 'onair.wsgi.application'
