"""URLs for the ``django-tinylinks`` app."""
from django.conf.urls import url
from django.views.generic import TemplateView

from .views import (
    StatisticsView,
    TinylinkCreateView,
    TinylinkDeleteView,
    TinylinkListView,
    TinylinkRedirectView,
    TinylinkUpdateView,
)


urlpatterns = [
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
        r'^update/(?P<pk>\d+)/(?P<mode>[a-z-]+)/$',
        TinylinkUpdateView.as_view(),
        name='tinylink_update',
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
        r'^statistics/?$',
        StatisticsView.as_view(),
        name='tinylink_statistics',
    ),

    url(
        r'^(?P<short_url>[a-zA-Z0-9-]+)/?$',
        TinylinkRedirectView.as_view(),
        name='tinylink_redirect',
    ),
]
