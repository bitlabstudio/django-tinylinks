"""Tests for the ``check_tinylink_targets`` admin command."""
from django.core import management
from django.test import TestCase

from tinylinks.models import Tinylink
from tinylinks.tests.factories import TinylinkFactory


class CommandTestCase(TestCase):
    """Test class for the ``check_tinylink_targets`` admin command."""
    longMessage = True

    def setUp(self):
        """Prepares the testing environment."""
        # database setup
        self.tinylink_valid = TinylinkFactory(long_url="http://www.google.com")
        self.tinylink_invalid = TinylinkFactory(
            long_url="http://www.a1b2c3d4e5000.com:8888/",
            short_url="cf7GDS",
        )

    def test_command(self):
        """Tests a full run of the custom admin command."""
        management.call_command('check_tinylink_targets')
        # Run twice, because just one link is checked per interval
        management.call_command('check_tinylink_targets')
        self.assertTrue(
            Tinylink.objects.get(pk=self.tinylink_invalid.id).is_broken,
            msg=('Should still be broken.'),
        )
        self.assertFalse(
            Tinylink.objects.get(pk=self.tinylink_valid.id).is_broken,
            msg=('Should be set to not broken.'),
        )
