"""Tests for the views of the ``django-tinylinks`` app."""
from django.contrib.auth.models import Permission
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin
from tinylinks.tests.factories import TinylinkFactory


class TinylinkViewTestsMixin(object):
    def setUp(self):
        self.user = UserFactory()
        # User needs this permission to access the create view.
        self.user.user_permissions.add(Permission.objects.get(
            codename="add_tinylink"))
        self.tinylink = TinylinkFactory()


class TinylinkCreateViewTestCase(TinylinkViewTestsMixin, ViewTestMixin,
                                 TestCase):
    """Tests for the ``TinylinkCreateView`` generic view class."""
    def get_view_name(self):
        return 'tinylink_create'

    def test_view(self):
        self.should_be_callable_when_authenticated(self.user)
        resp = self.client.post(self.get_url(),
                data={'long_url': 'http://www.example.com/foobar'})
        # User is redirected to a predefined form.
        # She can change the short URL or add a more readable one.
        self.assertRedirects(
            resp,
            reverse('tinylink_create_prefilled', kwargs={
                'link_id': self.tinylink.id + 1}),
            msg_prefix=('Should redirect to pre-filled create view.')
        )


class TinylinkPrefilledCreateViewTestCase(TinylinkViewTestsMixin, ViewTestMixin,
                                 TestCase):
    """
    Tests for the ``TinylinkCreateView`` generic view class.

    This time we add an optional parameter.
    """
    def get_view_name(self):
        return 'tinylink_create_prefilled'

    def get_view_kwargs(self):
        return {'link_id': 22}

    def test_view(self):
        self.login(self.user)
        resp = self.client.get(self.get_url())
        # We only test the redirect, if a "prefill"-id is non-existing.
        self.assertRedirects(resp, reverse('tinylink_create'), msg_prefix=(
            'Should redirect to create view if the id matches no instance.'))


class TinylinkRedirectViewTestCase(TinylinkViewTestsMixin, ViewTestMixin,
                                   TestCase):
    """
    Tests for the ``TinylinkRedirectView`` generic view class.

    """
    def get_view_name(self):
        return 'tinylink_redirect'

    def get_view_kwargs(self):
        return {'short_url': self.tinylink.short_url}

    def test_view(self):
        self.login(self.user)
        resp = self.client.get(self.get_url())
        # Valid redirection to long URL.
        self.assertEqual(
            resp.get('Location'),
            self.tinylink.long_url,
            msg=('Should redirect to long url. Response was {0}'.format(resp)))

        # Invalid short URL. Send to a 404-like template.
        resp = self.client.get('/s/aaaaa/')
        self.assertEqual(
            resp.get('Location'),
            'http://testserver{0}'.format(reverse('tinylink_notfound')),
            msg=('Should redirect to "Not found" page if short_url is'
                 ' inexistent. Response was {0}'.format(resp.get('Location'))))
