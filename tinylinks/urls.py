"""URLs for the ``django-tinylinks`` app."""
from django.conf.urls.defaults import include, patterns, url
# from django.contrib import admin
from django.views.generic import TemplateView

from tinylinks.views import TinylinkCreateView, TinylinkRedirectView


urlpatterns = patterns('',
    url(r'^$',
        TinylinkCreateView.as_view(),
        name='tinylink_create'
    ),

    url(r'^create/(?P<link_id>\d+)/$',
        TinylinkCreateView.as_view(),
        name='tinylink_create_prefilled',
    ),

    url(r'^404/$',
        TemplateView.as_view(template_name='tinylinks/notfound.html'),
        name='tinylink_notfound',
    ),

    url(r'^(?P<short_url>[a-zA-Z0-9-]+)/$',
        TinylinkRedirectView.as_view(),
        name='tinylink_redirect',
    ),

)
