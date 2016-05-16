"""Tests for the models of the ``django-tinylinks`` app."""
from django.test import TestCase, LiveServerTestCase
from django.utils.timezone import now, timedelta

from mixer.backend.django import mixer


class TinylinkTestCase(TestCase, LiveServerTestCase):
    """Tests for the ``Tinylink`` model class."""
    def setUp(self):
        self.link = mixer.blend(
            'tinylinks.TinyLink', short_url="vB7f5b",
            long_url="http://www.example.com/thisisalongURL")

    def test_model(self):
        self.assertTrue(str(self.link))

    def test_can_be_validated(self):
        self.assertFalse(self.link.can_be_validated())
        self.link.last_checked = now() - timedelta(minutes=61)
        self.assertTrue(self.link.can_be_validated())
