"""
Custom admin command to check all tinylink target URLs.

It should check in a certain interval during a certain period defined in the
settings by TINYLINK_CHECK_INTERVAL and TINYLINK_CHECK_PERIOD.
After one period, all URLs should be checked for their availability.

"""
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import Tinylink
from ...utils import validate_long_url


class Command(BaseCommand):
    """Class for the check_tinylink_targets admin command."""
    def handle(self, *args, **options):
        """Handles the check_tinylink_targets admin command."""
        interval = settings.TINYLINK_CHECK_INTERVAL
        period = settings.TINYLINK_CHECK_PERIOD
        url_amount = Tinylink.objects.all().count()
        check_amount = (url_amount / (period / interval)) or 1
        for link in Tinylink.objects.order_by('last_checked')[:check_amount]:
            validate_long_url(link)
        print('[' + timezone.now().strftime('%d.%m.%Y - %H:%M') +
              '] Checked ' + str(check_amount) + ' of ' + str(url_amount) +
              ' total URLs.')
