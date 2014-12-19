"""Models for the ``django-tinylinks`` app."""
import urllib2
from cookielib import CookieJar
from socket import gaierror

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from urllib3 import PoolManager
from urllib3.exceptions import HTTPError, MaxRetryError, TimeoutError


def get_url_response(pool, link, url):
    """
    Function to open and check an URL. In case of failure it sets the relevant
    validation error.

    """
    response = False
    link.is_broken = True
    link.redirect_location = ''
    # Try to encode e.g. chinese letters
    try:
        url = url.encode('utf-8')
    except UnicodeEncodeError:
        link.validation_error = _('Unicode error. Check URL characters.')
        return False
    try:
        response = pool.urlopen('GET', url, retries=2, timeout=8.0)
    except TimeoutError:
        link.validation_error = _('Timeout after 8 seconds.')
    except MaxRetryError:
        link.validation_error = _('Failed after retrying twice.')
    except (HTTPError, gaierror):
        link.validation_error = _('Not found.')
    return response


def validate_long_url(link):
    """
    Function to validate a URL. The validator uses urllib3 to test the URL's
    availability.

    """
    http = PoolManager()
    response = get_url_response(http, link, link.long_url)
    if response and response.status == 200:
        link.is_broken = False
    elif response and response.status == 302:
        # If link is redirected, validate the redirect location.
        if link.long_url.endswith('.pdf'):
            # Non-save pdf exception, to avoid relative path redirects
            link.is_broken = False
        else:
            redirect_location = response.get_redirect_location()
            redirect = get_url_response(http, link, redirect_location)
            link.redirect_location = redirect_location
            if redirect.status == 200:
                link.is_broken = False
            elif redirect.status == 302:
                # Seems like an infinite loop. Maybe the server is looking for
                # a cookie?
                cj = CookieJar()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                request = urllib2.Request(response.get_redirect_location())
                response = opener.open(request)
                if response.code == 200:
                    link.is_broken = False
    elif response and response.status == 502:
        # Sometimes urllib3 repond with a 502er. Those pages might respond with
        # a 200er in the Browser, so re-check with urllib2
        try:
            response = urllib2.urlopen(link.long_url, timeout=8.0)
        except urllib2.HTTPError:
            link.validation_error = _("URL not accessible.")
        else:
            link.is_broken = False
    else:
        link.validation_error = _("URL not accessible.")
    link.last_checked = timezone.now()
    link.save()
    return link


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
        default=timezone.now(),
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

    def __unicode__(self):
        return self.short_url

    class Meta:
        ordering = ['-id']

    def can_be_validated(self):
        """
        URL can only be validated if the last validation was at least 1
        hour ago

        """
        if self.last_checked < timezone.now() - timezone.timedelta(minutes=60):
            return True
        return False
