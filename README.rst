Django Tinylinks
================

A Django application that adds an URL shortener to your site similar to bit.ly.

Installation
------------

You need to install the following prerequisites in order to use this app::

    pip install django
    pip install requests

When using Python 2.6, you will also need to install importlib.

If you want to install the latest stable release from PyPi::

    $ pip install django-tinylinks

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-tinylinks.git#egg=tinylinks

Add ``tinylinks`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'tinylinks',
    )

Add the ``tinylinks`` URLs to your ``urls.py``::

    urlpatterns = [
        url(r'^s/', include('tinylinks.urls')),
    ]

Don't forget to migrate your database::

    ./manage.py migrate tinylinks

Settings
--------

TINYLINK_LENGTH
+++++++++++++++

Default: 6

Integer representing the number of characters for your tinylinks. This setting
is used when the app suggests a new tinylink. Regardless of this setting users
will be able to create custom tinylinks with up to 32 characters.


TINYLINK_CHECK_INTERVAL
+++++++++++++++++++++++

Default: 10

Number of minutes between two runs of the check command. This number should be
big enough so that one run can complete before the next run is scheduled.

TINYLINK_CHECK_PERIOD
+++++++++++++++++++++

Default: 300

Number of minutes in which all URLs should have been updated at least
once. If this is 300 it means that within 5 hours we want to update all URLs.

If ``TINYLINK_CHECK_INTERVAL`` is 10 it means that we will run the command
every 10 minutes. Combined with a total time of 300 minutes, this means that we
can execute the command 300/10=30 times during one period.

Now we can devide the total number of URLs by 30 and on each run we will
update the X most recent URLs. After 10 runs, we will have updated all URLs.

Usage
-----

Just visit the root URL of the app. Let's assume you hooked the app into your
``urls.py`` at `s/`, then visit `yoursite.com/s/`. You will see your tinylist
overview. Go to `yoursite.com/s/create/` to see a form to submit a new long URL.

After submitting, you will be redirected to a new page which shows the
generated short URL. If you want this URL to have a different short URL, just
change the short URL to your liking.

Now visit `yoursite.com/s/yourshorturl` and you will be redirected to your long
URL.

Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-tinylinks
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch

In order to run the tests, simply execute ``tox``. This will install two new
environments (for Django 1.8 and Django 1.9) and run the tests against both
environments.
