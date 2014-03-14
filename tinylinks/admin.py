"""Admin sites for the ``django-tinylinks`` app."""
from django.contrib import admin

from tinylinks.forms import TinylinkAdminForm
from tinylinks.models import Tinylink


class TinylinkAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'long_url', 'amount_of_views', 'user',
                    'last_checked')
    search_fields = ['short_url', 'long_url']
    form = TinylinkAdminForm


admin.site.register(Tinylink, TinylinkAdmin)
