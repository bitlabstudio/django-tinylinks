"""Tests for the forms of the ``django-tinylinks`` app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory

from tinylinks.forms import TinylinkForm
from tinylinks.models import Tinylink


class TinylinkFormTestCase(TestCase):
    """Test for the ``TinylinkForm`` form class."""
    def test_validates_saves(self):
        # Testing if the new link is saved.
        user = UserFactory()
        data = {'long_url': 'http://www.example.com/FooBar'}

        form = TinylinkForm(data=data, user=user)

        self.assertTrue(form.is_valid(), msg=(
            'If given correct data, the form should be valid.'))
        form.save()
        self.assertEqual(Tinylink.objects.all().count(), 1, msg=(
            'When save is called, there should be one link in the database.'
            ' Got {0}'.format(Tinylink.objects.all().count())))

        # Testing a 'Twin' submit, if the old inputs matches the new ones.
        tinylink = Tinylink.objects.get(pk=1)
        data.update({'short_url': tinylink.short_url})
        form = TinylinkForm(data=data, user=user)
        self.assertTrue(form.is_valid(), msg=(
            'If given correct data, the form should be valid.'))
        form.save()
        self.assertEqual(Tinylink.objects.all().count(), 1, msg=(
            'When saving with equal values, there should be no new tinylink'
            ' in the. database. Got {0}'.format(
                Tinylink.objects.all().count())))

        # Testing an input with a new short URL. Now, there are two tinylinks
        # with the same long_url.
        data.update({'short_url': 'FooBar01'})
        form = TinylinkForm(data=data, user=user)
        self.assertTrue(form.is_valid(), msg=(
            'If given correct data, the form should be valid.'))
        form.save()
        self.assertEqual(Tinylink.objects.all().count(), 2, msg=(
            'When saving with a new short url, there should be one new'
            ' tinylink in the database. Got {0}'.format(
                Tinylink.objects.all().count())))

        # Testing the input of an old long URL. There's no new submission,
        # only a redirect to the old entity, where this one can be changed.
        form = TinylinkForm(data={'long_url': data['long_url']}, user=user)
        self.assertTrue(form.is_valid(), msg=(
            'If given correct data, the form should be valid.'))
        form.save()
        self.assertEqual(Tinylink.objects.all().count(), 2, msg=(
            'When saving with no short url and the same long url, there is no'
            ' savement. The user is directed to the already existing tinylink.'
            ' Got {0}'.format(Tinylink.objects.all().count())))
