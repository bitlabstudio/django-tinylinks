"""Utils for the ``tinylinks`` app."""
from socket import gaierror

from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

import requests
from urllib3.exceptions import TimeoutError


def get_url_response(link, url):
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
        response = requests.get(url)
    except TimeoutError:
        link.validation_error = _('Timeout.')
    except requests.ConnectionError:
        link.validation_error = _('Failed after retrying.')
    except (requests.HTTPError, gaierror):
        link.validation_error = _('Not found.')
    return response, link


def validate_long_url(link):
    """
    Function to validate a URL. The validator uses urllib3 to test the URL's
    availability.

    """
    response, link = get_url_response(link, link.long_url)
    if response and response.status_code == 200:
        link.is_broken = False
    elif response and response.status_code == 302:
        # If link is redirected, validate the redirect location.
        if link.long_url.endswith('.pdf'):
            # Non-save pdf exception, to avoid relative path redirects
            link.is_broken = False
        else:
            redirect_location = response.get_redirect_location()
            redirect, link = get_url_response(link, redirect_location)
            link.redirect_location = redirect_location
            if redirect.status_code == 200:
                link.is_broken = False
            elif redirect.status_code == 302:
                # Seems like an infinite loop. Maybe the server is looking for
                # a cookie?
                response = requests.get(response.get_redirect_location())
                if response.status_code == 200:
                    link.is_broken = False
    elif response and response.status_code == 502:
        # Sometimes urllib3 repond with a 502er. Those pages might respond with
        # a 200er in the Browser, so re-check with urllib2
        try:
            requests.get(link.long_url)
        except requests.HTTPError:
            link.validation_error = _("URL not accessible.")
        else:
            link.is_broken = False
    else:
        link.validation_error = _("URL not accessible.")
    link.last_checked = now()
    link.save()
    return link
