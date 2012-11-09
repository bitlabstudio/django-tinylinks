"""Models for the ``django-tinylinks`` app."""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Tinylink(models.Model):
    """
    Model to 'translate' long URLs into small ones.

    :long_url: Long URL version.
    :short_url: Shortened URL.

    """
    long_url = models.CharField(
        max_length=2500,
        verbose_name=_('Long URL'),
    )

    short_url = models.CharField(
        max_length=32,
        verbose_name=_('Short URL'),
        unique=True,
    )
