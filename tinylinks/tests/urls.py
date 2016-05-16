"""
This ``urls.py`` is only used when running the tests via ``runtests.py``.
As you know, every app must be hooked into yout main ``urls.py`` so that
you can actually reach the app's views (provided it has any views, of course).

"""
from django.conf.urls import include, url
from django.contrib import admin

from . import views


admin.autodiscover()


urlpatterns = [
    url(r'^test/$', views.TestView.as_view(), name='test_view'),
    url(r'^redirect-test/$', views.TestRedirectView.as_view(),
        name='test_redirect'),
    url(r'^redirect-fail/$', views.TestFailedRedirectView.as_view(),
        name='test_redirect_fail'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('tinylinks.urls')),
]
