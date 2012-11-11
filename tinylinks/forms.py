"""Forms for the ``django-tinylinks`` app."""
import random

from django import forms
from django.conf import settings

from tinylinks.models import Tinylink


class TinylinkForm(forms.ModelForm):
    """
    Creates and validates long and short URL version.

    """
    def __init__(self, tinylink=None, *args, **kwargs):
        """
        The Regex field validates the URL input. Allowed are only slugified
        inputs.

        Examples:
        "D834n-qNx2q-jn" <- valid
        "D834n qNx2q jn" <- invalid
        "D834n_qNx2q/jn" <- invalid
        """
        super(TinylinkForm, self).__init__(*args, **kwargs)
        # tinylink is an instance. If there's none, hide the short URL field
        # to auto-generate a new instance.
        if not tinylink:
            self.fields['short_url'].widget = forms.HiddenInput()
            self.fields['short_url'].required = False
        else:
            # If there's an instance, paste the old values.
            self.initial = {
                'long_url': tinylink.long_url,
                'short_url': tinylink.short_url,
            }
            self.fields['short_url'] = forms.RegexField(
                regex=r'^[a-zA-Z0-9-]+$',
                error_message=("Please use only letters and digits."),
            )
        self.fields['long_url'] = forms.URLField()

    def clean(self):
        """

        """
        self.cleaned_data = super(TinylinkForm, self).clean()
        # Brothers are entities with the same long URL
        brothers = Tinylink.objects.filter(long_url=self.cleaned_data.get(
            'long_url'))
        input_url = self.cleaned_data.get('short_url')
        # Twins are to entities with the same values. The second new one should
        # not be saved.
        twin = brothers.filter(short_url=input_url)

        # Only handle with older brothers, if there's no new short URL value
        if (brothers and not input_url
            or twin and input_url == twin[0].short_url):
            if twin:
                # Twin will be saved, but with no new values.
                self.instance = twin[0]
            else:
                # This can only happen, if a user tries to auto-generate a
                # short URL with an existing tinylink. She will receive the
                # prefilled form with the link's old values.
                self.instance = brothers[0]
                self.cleaned_data.update(
                    {'short_url': self.instance.short_url})
        else:
            slug = ''
            if input_url:
                # User can customize their URLs
                slug = input_url
            # This keeps the unique validation of the short URLs alive.
            if not Tinylink.objects.filter(short_url=input_url):
                while not slug or Tinylink.objects.filter(short_url=slug):
                    slug = ''.join(random.choice(
                        'abcdefghijkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ1234'
                        '56789-') for x in range(
                            getattr(settings, 'TINYLINK_LENGTH', 6)))
                self.cleaned_data.update({'short_url': slug})
        return self.cleaned_data

    class Meta:
        model = Tinylink
