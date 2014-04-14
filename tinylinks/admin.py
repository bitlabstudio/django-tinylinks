"""Admin sites for the ``django-tinylinks`` app."""
from django.contrib import admin
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _

from tinylinks.forms import TinylinkAdminForm
from tinylinks.models import Tinylink


class TinylinkAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'url_truncated', 'amount_of_views', 'user',
                    'last_checked', 'status', 'validation_error')
    search_fields = ['short_url', 'long_url']
    form = TinylinkAdminForm

    def url_truncated(self, obj):
        return truncatechars(obj.long_url, 60)
    url_truncated.short_description = _('Long URL')

    def status(self, obj):
        if not obj.is_broken:
            return _('OK')
        return _('Link broken')
    status.short_description = _('Status')


admin.site.register(Tinylink, TinylinkAdmin)
