"""URLs for the ``django-tinylinks`` app."""
from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView

from tinylinks.views import (
    TinylinkCreateView,
    TinylinkDeleteView,
    TinylinkListView,
    TinylinkRedirectView,
)


urlpatterns = patterns(
    '',
    url(
        r'^$',
        TinylinkListView.as_view(),
        name='tinylink_list'
    ),

    url(
        r'^create/$',
        TinylinkCreateView.as_view(),
        name='tinylink_create'
    ),

    url(
        r'^update/(?P<link_id>\d+)/$',
        TinylinkCreateView.as_view(),
        name='tinylink_create_prefilled',
    ),

    url(
        r'^delete/(?P<pk>\d+)/$',
        TinylinkDeleteView.as_view(),
        name='tinylink_delete',
    ),

    url(
        r'^404/$',
        TemplateView.as_view(template_name='tinylinks/notfound.html'),
        name='tinylink_notfound',
    ),

    url(
        r'^(?P<short_url>[a-zA-Z0-9-]+)/?$',
        TinylinkRedirectView.as_view(),
        name='tinylink_redirect',
    ),

)
