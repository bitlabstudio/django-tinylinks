"""Tests for the ``check_tinylink_targets`` admin command."""
from django.core import management
from django.core.urlresolvers import reverse
from django.test import TestCase, LiveServerTestCase

from mixer.backend.django import mixer
from mock import patch
from requests import Response

from ..models import Tinylink


class CommandTestCase(TestCase, LiveServerTestCase):
    """Test class for the ``check_tinylink_targets`` admin command."""
    longMessage = True

    def setUp(self):
        """Prepares the testing environment."""
        # database setup
        self.tinylink1 = mixer.blend(
            'tinylinks.TinyLink', short_url="vB7f5b",
            long_url='{}{}'.format(self.live_server_url, reverse('test_view')))
        self.tinylink2 = mixer.blend(
            'tinylinks.TinyLink',
            long_url='http://foobar.foobar',
            short_url="cf7GDS",
        )

    @patch('requests.get')
    def test_command(self, mock):
        resp = Response()
        resp.status_code = 200
        mock.return_value = resp

        management.call_command('check_tinylink_targets')
        # Run twice, because just one link is checked per interval
        management.call_command('check_tinylink_targets')
        self.assertFalse(
            Tinylink.objects.get(pk=self.tinylink1.id).is_broken,
            msg=('Should not be broken.'),
        )
        self.assertFalse(
            Tinylink.objects.get(pk=self.tinylink2.id).is_broken,
            msg=('Should not be broken.'),
        )
