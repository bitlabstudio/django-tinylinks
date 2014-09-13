"""Settings that need to be set in order to run the tests."""
import logging
import os


logging.getLogger("factory").setLevel(logging.WARN)
logging.getLogger("urllib3").setLevel(logging.WARN)

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

TEMPLATE_DIRS = (
    os.path.join(CURRENT_DIR, '../templates'),
)

JASMINE_TEST_DIRECTORY = os.path.join(CURRENT_DIR, 'jasmine_tests')

COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(
    CURRENT_DIR, 'coverage')

COVERAGE_MODULE_EXCLUDES = [
    'tests$', 'test_app$', 'settings$', 'urls$', 'locale$',
    'migrations', 'fixtures', 'admin$', 'django_extensions',
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
    'django_jasmine',
    'django_libs',
]

INTERNAL_APPS = [
    'django_nose',
    'tinylinks.tests.test_app',
    'tinylinks',
]

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS

COVERAGE_MODULE_EXCLUDES += EXTERNAL_APPS
