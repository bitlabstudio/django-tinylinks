"""Tests for the views of the ``django-tinylinks`` app."""
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.core.urlresolvers import reverse

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin
from tinylinks.models import Tinylink
from tinylinks.tests.factories import TinylinkFactory


class TinylinkViewTestsMixin(object):
    def setUp(self):
        self.user = UserFactory()
        # User needs this permission to access the create view.
        self.user.user_permissions.add(Permission.objects.get(
            codename="add_tinylink"))
        self.user.user_permissions.add(Permission.objects.get(
            codename="delete_tinylink"))
        self.tinylink = TinylinkFactory(user=self.user)
        self.second_user = UserFactory()
        self.second_user.user_permissions.add(Permission.objects.get(
            codename="add_tinylink"))
        self.second_user.user_permissions.add(Permission.objects.get(
            codename="delete_tinylink"))
        self.staff = UserFactory(is_staff=True, is_superuser=True)


class TinylinkListViewTestCase(TinylinkViewTestsMixin, ViewTestMixin,
                               TestCase):
    """Tests for the ``TinylinkListView`` generic view class."""
    def get_view_name(self):
        return 'tinylink_list'

    def test_view(self):
        self.should_be_callable_when_authenticated(self.staff)
        self.should_be_callable_when_authenticated(self.user)
        resp = self.client.post(self.get_url(), data={'validateABC': True})
        self.assertEqual(resp.status_code, 404, msg=(
            'Should raise a 404 if pk is not a number. Status was {0}.'.format(
                resp.status_code)))
        resp = self.client.post(self.get_url(), data={'validate999': True})
        self.assertEqual(resp.status_code, 404, msg=(
            'Should raise a 404 if pk is non-existent. Status was {0}.'.format(
                resp.status_code)))
        self.tinylink.long_url = "http://www.google.com"
        self.tinylink.is_broken = True
        self.tinylink.save()
        self.client.post(self.get_url(), data={
            'validate{0}'.format(self.tinylink.id): True})
        self.assertFalse(Tinylink.objects.get(pk=self.tinylink.pk).is_broken,
                         msg="Link should be valid.")


class TinylinkCreateViewTestCase(TinylinkViewTestsMixin, ViewTestMixin,
                                 TestCase):
    """Tests for the ``TinylinkCreateView`` generic view class."""
    def get_view_name(self):
        return 'tinylink_create'

    def test_view(self):
        self.should_be_callable_when_authenticated(self.user)
        resp = self.client.post(
            self.get_url(),
            data={'long_url': 'http://www.example.com/foobar'},
        )
        # User is redirected to a predefined form.
        # She can change the short URL or add a more readable one.
        self.assertRedirects(
            resp,
            reverse('tinylink_update', kwargs={'pk': self.tinylink.id + 1,
                                               'mode': 'change-short'}),
            msg_prefix=('Should redirect to pre-filled create view.')
        )


class TinylinkUpdateViewTestCase(TinylinkViewTestsMixin, ViewTestMixin,
                                 TestCase):
    """
    Tests for the ``TinylinkUpdateView`` generic view class.

    """
    def get_view_name(self):
        return 'tinylink_update'

    def get_view_kwargs(self):
        return {'pk': self.tinylink.id, 'mode': 'change-short'}

    def test_view(self):
        self.login(self.user)
        # Redirect to list after saving.
        data = {
            'long_url': self.tinylink.long_url,
            'short_url': 'foobar',
        }
        resp = self.client.post(self.get_url(), data=data)
        self.assertRedirects(resp, reverse('tinylink_list'), msg_prefix=(
            'Should redirect to list.'))


class TinylinkDeleteViewTestCase(TinylinkViewTestsMixin, ViewTestMixin,
                                 TestCase):
    """Tests for the ``TinylinkDeleteView`` generic view class."""
    def get_view_name(self):
        return 'tinylink_delete'

    def get_view_kwargs(self):
        return {'pk': self.tinylink.id}

    def test_view(self):
        # Raise 404 if user is not author of the tinylink.
        self.login(self.second_user)
        resp = self.client.get(self.get_url())
        self.assertEqual(resp.status_code, 404, msg=(
            'Should raise a 404 if user is not owner of the tinylink. Status'
            ' was {0}.'.format(resp.status_code)))
        self.should_be_callable_when_authenticated(self.user)
        resp = self.client.post(self.get_url(), data={'Foo': 'Bar'})
        self.assertRedirects(resp, reverse('tinylink_list'), msg_prefix=(
            'Should redirect to list view if the tinylink has been deleted.'))


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
        view_amount = Tinylink.objects.get(pk=self.tinylink.pk).amount_of_views
        self.assertEqual(view_amount, 1, msg=(
            'Should set the view amount to 1. Amount:{0}'.format(view_amount)))
        # Invalid short URL. Send to a 404-like template.
        resp = self.client.get('/aaaaa/')
        self.assertEqual(
            resp.get('Location'),
            'http://testserver{0}'.format(reverse('tinylink_notfound')),
            msg=('Should redirect to "Not found" page if short_url is'
                 ' inexistent. Response was {0}'.format(resp.get('Location'))))

    def test_can_handle_urls_with_percent_characters(self):
        """Regression test due to reported internal server errors."""
        tinylink = TinylinkFactory(
            user=self.user, long_url='http://www.example.com/test%20Efile.pdf',
            short_url='abcdef')
        self.login(self.user)
        resp = self.client.get(self.get_url(
            view_kwargs={'short_url': tinylink.short_url, }))
        self.assertEqual(
            resp.get('Location'),
            tinylink.long_url,
            msg=('Should redirect to long url. Response was {0}'.format(resp)))


class StatisticsViewTestCase(TinylinkViewTestsMixin, ViewTestMixin, TestCase):
    """Tests for the ``StatisticsView`` generic view class."""
    def get_view_name(self):
        return 'tinylink_statistics'

    def test_view(self):
        self.login(self.user)
        resp = self.client.get(self.get_url())
        self.assertEqual(resp.status_code, 404, msg=(
            'Should only be accessible for staff users. Status: {0}.'.format(
                resp.status_code)))
        self.user.is_staff = True
        self.user.save()
        self.should_be_callable_when_authenticated(self.user)
