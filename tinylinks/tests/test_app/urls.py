"""
URLs for the test_app of ``django-tinylinks``.

Allows us to run `./manage.py runserver` and see a form that uses the tag
functionality. This helps testing the JavaScript related parts of this app
without needing to setup a full blown Django project.

"""
from django.conf.urls.defaults import include, patterns, url


urlpatterns = patterns('',
    url(r'^', include('tinylinks.urls')),
)
