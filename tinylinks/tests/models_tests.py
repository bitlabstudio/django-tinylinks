"""Tests for the models of the ``django-tinylinks`` app."""
from django.test import TestCase

from tinylinks.tests.factories import TinylinkFactory


class TinylinkTestCase(TestCase):
    """Tests for the ``Tinylink`` model class."""
    def test_model(self):
        obj = TinylinkFactory()
        self.assertTrue(obj.pk)
