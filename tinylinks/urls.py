"""URLs for the ``django-tinylinks`` app."""
from django.conf.urls.defaults import include, patterns, url
# from django.contrib import admin
from django.views.generic import TemplateView

from tinylinks.views import TinylinkCreateView, TinylinkRedirectView


urlpatterns = patterns('',
    # url(r'^', include(admin.site.urls)),
    url(
        r'^s/404/$',
        TemplateView.as_view(template_name='tinylinks/notfound.html'),
        name='tinylink_notfound',
    ),

    url(
        r'^s/(?P<short_url>[a-zA-Z0-9-]+)/$',
        TinylinkRedirectView.as_view(),
        name='tinylink_redirect',
    ),

    url(
        r'^(?P<link_id>\d+)/$',
        TinylinkCreateView.as_view(),
        name='tinylink_create_prefilled',
    ),

    url(r'^$', TinylinkCreateView.as_view(), name='tinylink_create'),
)
