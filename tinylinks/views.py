"""Views for the ``django-tinylinks`` application."""
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    RedirectView,
    UpdateView,
)

from .forms import TinylinkForm
from .models import Tinylink
from .utils import validate_long_url


class TinylinkViewMixin(object):
    """
    View to handle general functions for Tinylink objects.

    """
    model = Tinylink
    form_class = TinylinkForm

    @method_decorator(permission_required('tinylinks.add_tinylink'))
    def dispatch(self, *args, **kwargs):
        self.mode = kwargs.get('mode')
        return super(TinylinkViewMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TinylinkViewMixin, self).get_context_data(**kwargs)
        context.update({'mode': self.mode})
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        if hasattr(self, 'get_object') and kwargs.get('pk'):
            self.object = self.get_object()
            if ((not self.object or self.object.user != request.user) and not
                    request.user.is_staff):
                raise Http404
        return super(TinylinkViewMixin, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TinylinkViewMixin, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
            'mode': self.mode,
        })
        return kwargs

    def get_success_url(self):
        return reverse('tinylink_list')


class TinylinkListView(TinylinkViewMixin, ListView):
    """
    View to list all tinylinks of a user.

    """
    def post(self, request, *args, **kwargs):
        for key in request.POST:
            if key.startswith('validate'):
                try:
                    link_id = int(key.replace('validate', ''))
                except ValueError:
                    raise Http404
                try:
                    link = Tinylink.objects.get(pk=link_id)
                except Tinylink.DoesNotExist:
                    raise Http404
                validate_long_url(link)
        return super(TinylinkListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Tinylink.objects.all()
        return self.request.user.tinylinks.all()


class TinylinkCreateView(TinylinkViewMixin, CreateView):
    """
    View to generate a Tinylink instance including a shortened URL.

    """
    def get_success_url(self):
        return reverse('tinylink_update', kwargs={'pk': self.object.id,
                                                  'mode': 'change-short'})


class TinylinkUpdateView(TinylinkViewMixin, UpdateView):
    """
    View to update a Tinylink instance.

    """
    pass


class TinylinkDeleteView(TinylinkViewMixin, DeleteView):
    """
    View to delete a certain tinylink.

    """
    pass


class TinylinkRedirectView(RedirectView):
    """
    View to validate a short URL and redirect to its location.

    """
    def dispatch(self, *args, **kwargs):
        try:
            tinylink = Tinylink.objects.get(short_url=kwargs.get(
                'short_url'))
        except Tinylink.DoesNotExist:
            tinylink = None
            self.url = reverse('tinylink_notfound')
        if tinylink:
            # set the redirect long URL
            self.url = tinylink.long_url
            tinylink.amount_of_views += 1
            tinylink.save()
        return super(TinylinkRedirectView, self).dispatch(*args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return self.url


class StatisticsView(ListView):
    """
    View to list all tinylinks including their statistics.

    """
    model = Tinylink
    template_name = "tinylinks/statistics.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(StatisticsView, self).dispatch(request, *args, **kwargs)
