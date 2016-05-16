"""Test views for the ``django-tinylinks`` application."""
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views.generic import RedirectView, View, TemplateView


class TestFailedRedirectView(View):
    def dispatch(self, *args, **kwargs):
        raise Http404


class TestView(TemplateView):
    template_name = 'base.html'


class TestRedirectView(RedirectView):
    url = reverse_lazy('tinylink_create')
    permanent = False
