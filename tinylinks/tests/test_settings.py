"""Settings that need to be set in order to run the tests."""
import os

DEBUG = True
USE_TZ = True
SITE_ID = 1

"""
TINYLINK_CHECK_INTERVAL
-----------------------

Number of minutes between two runs of the check command. This number should be
big enough so that one run can complete before the next run is scheduled.

TINYLINK_CHECK_PERIOD
---------------------

Number of minutes in which all URLs should have been updated at least
once. If this is 300 it means that within 5 hours we want to update all URLs.

If ``TINYLINK_CHECK_INTERVAL`` is 10 it means that we will run the command
every 10 minutes. Combined with a total time of 300 minutes, this means that we
can execute the command 300/10=30 times during one period.

Now we can devide the total number of URLs by 30 and on each run we will
update the X most recent URLs. After 10 runs, we will have updated all URLs.

TINYLINK_LENGTH
---------------

This is the length of the auto-generated short URLs. Keep it small, if
possible, otherwise this app is obsolete ;)

"""
TINYLINK_LENGTH = 5
TINYLINK_CHECK_INTERVAL = 1
TINYLINK_CHECK_PERIOD = 1

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
