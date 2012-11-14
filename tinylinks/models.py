"""Models for the ``django-tinylinks`` app."""
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now


def validate_long_url(link):
    """
    Function to valid a URL. The validator uses urllib2 to test the URL's
    availability.

    """
    validate = URLValidator(verify_exists=True)
    try:
        result = validate(link.long_url)
    except ValidationError:
        result = 'invalid'
    link.last_checked = now()
    if result == 'invalid':
        link.is_broken = True
    else:
        link.is_broken = False
    link.save()


class Tinylink(models.Model):
    """
    Model to 'translate' long URLs into small ones.

    :user: The author of the tinylink.
    :long_url: Long URL version.
    :short_url: Shortened URL.
    :is_broken: Set if the given long URL couldn't be validated.
    :last_checked: Datetime of the last validation process.
    :amount_of_views: Field to count the redirect views.

    """
    user = models.ForeignKey(
        'auth.User',
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

    last_checked = models.DateTimeField(
        default=now(),
        verbose_name=_('Last validation'),
    )

    amount_of_views = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Amount of views'),
    )

    def __unicode__(self):
        return self.short_url


def tinylink_post_save(sender, instance, created, *args, **kwargs):
    if created:
        validate_long_url(instance)

models.signals.post_save.connect(tinylink_post_save, sender=Tinylink)
