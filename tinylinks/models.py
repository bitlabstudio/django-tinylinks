"""Models for the ``django-tinylinks`` app."""
from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now, timedelta


@python_2_unicode_compatible
class Tinylink(models.Model):
    """
    Model to 'translate' long URLs into small ones.

    :user: The author of the tinylink.
    :long_url: Long URL version.
    :short_url: Shortened URL.
    :is_broken: Set if the given long URL couldn't be validated.
    :validation_error: Description of the occurred error.
    :last_checked: Datetime of the last validation process.
    :amount_of_views: Field to count the redirect views.
    :redirect_location: Redirect location if the long_url is redirected.

    """
    user = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        verbose_name=_('Author'),
        related_name="tinylinks",
    )

    long_url = models.CharField(
        max_length=2500,
        verbose_name=_('Long URL'),
    )

    short_url = models.CharField(
        max_length=32,
        verbose_name=_('Short URL'),
        unique=True,
    )

    is_broken = models.BooleanField(
        default=False,
        verbose_name=_('Status'),
    )

    validation_error = models.CharField(
        max_length=100,
        verbose_name=_('Validation Error'),
        default='',
    )

    last_checked = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Last validation'),
    )

    amount_of_views = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Amount of views'),
    )

    redirect_location = models.CharField(
        max_length=2500,
        verbose_name=_('Redirect location'),
        default='',
    )

    def __str__(self):
        return self.short_url

    class Meta:
        ordering = ['-pk']

    def can_be_validated(self):
        """
        URL can only be validated if the last validation was at least 1
        hour ago

        """
        if self.last_checked < now() - timedelta(minutes=60):
            return True
        return False
