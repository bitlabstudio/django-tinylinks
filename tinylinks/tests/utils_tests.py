"""Tests for the models of the ``django-tinylinks`` app."""
from django.core.urlresolvers import reverse
from django.test import TestCase, LiveServerTestCase

from mixer.backend.django import mixer

from ..models import Tinylink
from ..utils import validate_long_url


class ValidateLongUrlTestCase(TestCase, LiveServerTestCase):
    """Tests for the ``validate_long_url`` method."""
    def setUp(self):
        self.link = mixer.blend(
            'tinylinks.TinyLink', short_url="vB7f5b",
            long_url='{}{}'.format(self.live_server_url, reverse('test_view')))

    def test_method(self):
        validate_long_url(self.link)
        self.assertEqual(
            Tinylink.objects.get(pk=self.link.pk).validation_error, "")
        self.link.long_url = 'http://{}'.format(self.server_thread.host)
        self.link.save()
        validate_long_url(self.link)
        self.assertEqual(
            Tinylink.objects.get(pk=self.link.pk).validation_error,
            "URL not accessible.")
        self.link.long_url = '{}{}'.format(self.live_server_url,
                                           reverse('test_redirect_fail'))
        self.link.save()
        validate_long_url(self.link)
        self.assertTrue(Tinylink.objects.get(pk=self.link.pk).is_broken)
        self.link.long_url = '{}{}'.format(self.live_server_url,
                                           reverse('test_redirect'))
        self.link.save()
        validate_long_url(self.link)
        self.assertTrue(Tinylink.objects.get(pk=self.link.pk).is_broken)
