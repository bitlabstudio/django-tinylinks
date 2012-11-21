"""Views for the ``django-tinylinks`` application."""
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, RedirectView

from tinylinks.forms import TinylinkForm
from tinylinks.models import Tinylink


class TinylinkListView(ListView):
    """
    View to list all tinylinks of a user.

    """
    @method_decorator(permission_required('tinylinks.add_tinylink'))
    def dispatch(self, *args, **kwargs):
        return super(TinylinkListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Tinylink.objects.all()
        return self.request.user.tinylinks.all()


class TinylinkCreateView(CreateView):
    """
    View to generate a Tinylink instance including a shortened URL.

    """
    model = Tinylink
    form_class = TinylinkForm

    @method_decorator(permission_required('tinylinks.add_tinylink'))
    def dispatch(self, request, *args, **kwargs):
        self.tinylink = None
        if kwargs.get('link_id'):
            # Check if the form needs to be prefilled
            try:
                self.tinylink = Tinylink.objects.get(pk=kwargs.get('link_id'))
            except Tinylink.DoesNotExist:
                return HttpResponseRedirect(reverse('tinylink_create'))
            if not self.tinylink.user == request.user:
                return HttpResponseRedirect(reverse('tinylink_create'))
        return super(TinylinkCreateView, self).dispatch(request, *args,
                                                        **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TinylinkCreateView, self).get_form_kwargs()
        # Form prefill object
        kwargs.update({
            'user': self.request.user,
            'tinylink': self.tinylink,
        })
        return kwargs

    def get_success_url(self):
        if self.tinylink:
            return reverse('tinylink_list')
        return reverse('tinylink_create_prefilled', kwargs={
            'link_id': self.object.id})


class TinylinkDeleteView(DeleteView):
    """
    View to delete a certain tinylink.

    """
    model = Tinylink

    @method_decorator(permission_required('tinylinks.delete_tinylink'))
    def dispatch(self, request, *args, **kwargs):
        return super(TinylinkDeleteView, self).dispatch(request, *args,
                                                        **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object or not self.object.user == request.user:
            raise Http404
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('tinylink_list')


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
                tinylink.amount_of_views += 1
                tinylink.save()
        return super(TinylinkRedirectView, self).dispatch(*args, **kwargs)


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
