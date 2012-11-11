"""Views for the ``django-tinylinks`` application."""
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, RedirectView

from tinylinks.forms import TinylinkForm
from tinylinks.models import Tinylink


class TinylinkCreateView(CreateView):
    """
    View to generate a Tinylink instance including a shortened URL.

    """
    model = Tinylink
    form_class = TinylinkForm

    @method_decorator(permission_required('tinylinks.add_tinylink'))
    def dispatch(self, *args, **kwargs):
        self.tinylink = None
        if kwargs.get('link_id'):
            # Check if the form needs to be prefilled
            try:
                self.tinylink = Tinylink.objects.get(pk=kwargs.get('link_id'))
            except Tinylink.DoesNotExist:
                return HttpResponseRedirect(reverse('tinylink_create'))
        return super(TinylinkCreateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TinylinkCreateView, self).get_form_kwargs()
        # Form prefill object
        kwargs.update({'tinylink': self.tinylink})
        return kwargs

    def get_success_url(self):
        return reverse('tinylink_create_prefilled', kwargs={
            'link_id': self.object.id})


class TinylinkRedirectView(RedirectView):
    """
    View to validate a short URL and redirect to its location.

    """
    def dispatch(self, *args, **kwargs):
        if kwargs.get('short_url'):
            try:
                tinylink = Tinylink.objects.get(short_url=kwargs.get(
                    'short_url'))
            except Tinylink.DoesNotExist:
                tinylink = None
                self.url = reverse('tinylink_notfound')
            if tinylink:
                # set the redirect long URL
                self.url = tinylink.long_url
        return super(TinylinkRedirectView, self).dispatch(*args, **kwargs)
