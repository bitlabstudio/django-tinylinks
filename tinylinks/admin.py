"""Admin sites for the ``django-tinylinks`` app."""
from django.contrib import admin

from tinylinks.models import Tinylink


class TinylinkAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'long_url')


admin.site.register(Tinylink, TinylinkAdmin)
