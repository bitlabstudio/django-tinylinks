"""Settings that need to be set in order to run the tests."""
import os


DEBUG = True
USE_TZ = True
SITE_ID = 1

SECRET_KEY = "foobar"

TINYLINK_LENGTH = 5
TINYLINK_CHECK_INTERVAL = 10
TINYLINK_CHECK_PERIOD = 300

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

CURRENT_DIR = os.path.dirname(__file__)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = 'tinylinks.tests.urls'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(CURRENT_DIR, '../../static/')

STATICFILES_DIRS = (
    os.path.join(CURRENT_DIR, 'test_static'),
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'DIRS': [os.path.join(CURRENT_DIR, '../templates')],
    'OPTIONS': {
        'context_processors': (
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.request',
        )
    }
}]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]


EXTERNAL_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django_libs',
]

INTERNAL_APPS = [
    'tinylinks.tests.test_app',
    'tinylinks',
]

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS
