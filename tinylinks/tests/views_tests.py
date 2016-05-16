"""Tests for the views of the ``django-tinylinks`` app."""
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.core.urlresolvers import reverse

from django_libs.tests.mixins import ViewRequestFactoryTestMixin
from mixer.backend.django import mixer
from mock import patch
from requests import Response

from .. import views
from ..models import Tinylink


class TinylinkViewTestsMixin(object):
    def setUp(self):
        self.user = mixer.blend('auth.User')
        # User needs this permission to access the create view.
        self.user.user_permissions.add(Permission.objects.get(
            codename="add_tinylink"))
        self.user.user_permissions.add(Permission.objects.get(
            codename="delete_tinylink"))
        self.tinylink = mixer.blend(
            'tinylinks.TinyLink', short_url="vB7f5b",
            long_url="http://www.example.com/thisisalongURL", user=self.user)
        self.second_user = mixer.blend('auth.User')
        self.second_user.user_permissions.add(Permission.objects.get(
            codename="add_tinylink"))
        self.second_user.user_permissions.add(Permission.objects.get(
            codename="delete_tinylink"))
        self.staff = mixer.blend('auth.User', is_staff=True, is_superuser=True)


class TinylinkListViewTestCase(ViewRequestFactoryTestMixin,
                               TinylinkViewTestsMixin, TestCase):
    """Tests for the ``TinylinkListView`` generic view class."""
    view_class = views.TinylinkListView

    @patch('requests.get')
    def test_view(self, mock):
        resp = Response()
        resp.status_code = 200
        mock.return_value = resp

        self.is_callable(user=self.staff)
        self.is_callable(user=self.user)
        self.is_not_callable(user=self.user, data={'validateABC': True},
                             post=True)
        self.is_not_callable(user=self.user, data={'validate999': True},
                             post=True)
        self.tinylink.long_url = "http://www.google.com"
        self.tinylink.is_broken = True
        self.tinylink.save()
        self.is_postable(user=self.user, data={
            'validate{0}'.format(self.tinylink.id): True}, ajax=True)
        self.assertFalse(Tinylink.objects.get(pk=self.tinylink.pk).is_broken,
                         msg="Link should be valid.")


class TinylinkCreateViewTestCase(ViewRequestFactoryTestMixin,
                                 TinylinkViewTestsMixin, TestCase):
    """Tests for the ``TinylinkCreateView`` generic view class."""
    view_class = views.TinylinkCreateView

    def test_view(self):
        self.is_callable(user=self.user)
        # User is redirected to a predefined form.
        # She can change the short URL or add a more readable one.
        self.is_postable(user=self.user, to_url_name='tinylink_update', data={
            'long_url': 'http://www.example.com/foobar'})


class TinylinkUpdateViewTestCase(ViewRequestFactoryTestMixin,
                                 TinylinkViewTestsMixin, TestCase):
    """
    Tests for the ``TinylinkUpdateView`` generic view class.

    """
    view_class = views.TinylinkUpdateView

    def get_view_kwargs(self):
        return {'pk': self.tinylink.id, 'mode': 'change-short'}

    def test_view(self):
        self.login(self.user)
        # Redirect to list after saving.
        data = {
            'long_url': self.tinylink.long_url,
            'short_url': 'foobar',
        }
        self.is_postable(user=self.user, data=data,
                         to_url_name='tinylink_list')


class TinylinkDeleteViewTestCase(ViewRequestFactoryTestMixin,
                                 TinylinkViewTestsMixin, TestCase):
    """Tests for the ``TinylinkDeleteView`` generic view class."""
    view_class = views.TinylinkDeleteView

    def get_view_kwargs(self):
        return {'pk': self.tinylink.id}

    def test_view(self):
        # Raise 404 if user is not author of the tinylink.
        self.is_not_callable(user=self.second_user)
        self.is_callable(user=self.user)
        self.is_postable(user=self.user, data={'Foo': 'Bar'},
                         to_url_name='tinylink_list')


class TinylinkRedirectViewTestCase(ViewRequestFactoryTestMixin,
                                   TinylinkViewTestsMixin, TestCase):
    """
    Tests for the ``TinylinkRedirectView`` generic view class.

    """
    view_class = views.TinylinkRedirectView

    def get_view_kwargs(self):
        return {'short_url': self.tinylink.short_url}

    def test_view(self):
        resp = self.redirects(user=self.user)
        # Valid redirection to long URL.
        self.assertEqual(
            resp.get('Location'),
            self.tinylink.long_url,
            msg=('Should redirect to long url. Response was {0}'.format(resp)))
        view_amount = Tinylink.objects.get(pk=self.tinylink.pk).amount_of_views
        self.assertEqual(view_amount, 1, msg=(
            'Should set the view amount to 1. Amount:{0}'.format(view_amount)))
        # Invalid short URL. Send to a 404-like template.
        resp = self.client.get('/aaaaa/')
        self.assertIn(
            reverse('tinylink_notfound'),
            resp.get('Location'),
            msg=('Should redirect to "Not found" page if short_url is'
                 ' inexistent. Response was {0}'.format(resp.get('Location'))))

    def test_can_handle_urls_with_percent_characters(self):
        """Regression test due to reported internal server errors."""
        tinylink = mixer.blend(
            'tinylinks.TinyLink', user=self.user, short_url='abcdef',
            long_url='http://www.example.com/test%20Efile.pdf')
        resp = self.redirects(user=self.user, kwargs={
            'short_url': tinylink.short_url})
        self.assertEqual(
            resp.get('Location'),
            tinylink.long_url,
            msg=('Should redirect to long url. Response was {0}'.format(resp)))


class StatisticsViewTestCase(ViewRequestFactoryTestMixin,
                             TinylinkViewTestsMixin, TestCase):
    """Tests for the ``StatisticsView`` generic view class."""
    view_class = views.StatisticsView

    def test_view(self):
        self.is_not_callable(user=self.user)
        self.user.is_staff = True
        self.user.save()
        self.is_callable(user=self.user)
