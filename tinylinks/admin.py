"""Admin sites for the ``django-tinylinks`` app."""
from django.contrib import admin
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _

from tinylinks.forms import TinylinkAdminForm
from tinylinks.models import Tinylink


class TinylinkAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'url_truncated', 'amount_of_views', 'user',
                    'last_checked', 'is_broken', 'validation_error')
    search_fields = ['short_url', 'long_url']
    form = TinylinkAdminForm

    def url_truncated(self, obj):
        return truncatechars(obj.long_url, 60)
    url_truncated.short_description = _('Long URL')


admin.site.register(Tinylink, TinylinkAdmin)
