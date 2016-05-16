"""Forms for the ``django-tinylinks`` app."""
import random

from django import forms
from django.conf import settings
from django.forms.utils import ErrorList
from django.utils.translation import ugettext_lazy as _

from .models import Tinylink
from .utils import validate_long_url


class TinylinkForm(forms.ModelForm):
    """
    Creates and validates long and short URL version.

    """
    def __init__(self, user=None, mode='change-short', *args, **kwargs):
        """
        The Regex field validates the URL input. Allowed are only slugified
        inputs.

        Examples:
        "D834n-qNx2q-jn" <- valid
        "D834n qNx2q jn" <- invalid
        "D834n_qNx2q/jn" <- invalid
        """
        super(TinylinkForm, self).__init__(*args, **kwargs)
        if mode == 'change-long':
            long_help_text = _("You can now change your long URL.")
        else:
            long_help_text = _("The long URL isn't editable at the moment.")
        self.fields['long_url'] = forms.URLField(
            label=self.instance._meta.get_field('long_url').verbose_name,
            help_text=long_help_text,
        )
        if not self.instance.pk:
            # Hide the short URL field to auto-generate a new instance.
            self.fields['short_url'].widget = forms.HiddenInput()
            self.fields['short_url'].required = False
        else:
            # Dependent on the user mode, one URL field should not be editable.
            if mode == 'change-long':
                self.fields['short_url'].widget.attrs['readonly'] = True
                self.fields['short_url'].help_text = _(
                    "The short URL isn't editable at the moment.")
            else:
                self.fields['long_url'].widget.attrs['readonly'] = True
                self.fields['short_url'] = forms.RegexField(
                    regex=r'^[a-z0-9]+$',
                    help_text=_("You can add a more readable short URL."),
                    label=self.instance._meta.get_field(
                        'short_url').verbose_name,
                )
                self.fields['short_url'].error_messages['invalid'] = _(
                    "Please use only small letters and digits.")
        self.user = user

    def clean(self):
        self.cleaned_data = super(TinylinkForm, self).clean()
        # If short URL is occupied throw out an error, or fail silent.
        try:
            twin = Tinylink.objects.get(short_url=self.cleaned_data.get(
                'short_url'))
            if not self.instance == twin:
                self._errors['short_url'] = ErrorList([_(
                    'This short url already exists. Please try another one.')])
            return self.cleaned_data
        except Tinylink.DoesNotExist:
            pass
        # Brothers are entities with the same long URL
        brothers = Tinylink.objects.filter(long_url=self.cleaned_data.get(
            'long_url'), user=self.user)
        input_url = self.cleaned_data.get('short_url')

        # Only handle with older brothers, if there's no new short URL value
        if brothers and not input_url:
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
                    slug = ''.join(
                        random.choice('abcdefghijkmnpqrstuvwxyz123456789')
                        for x in range(
                            getattr(settings, 'TINYLINK_LENGTH', 6)))
                self.cleaned_data.update({'short_url': slug})
        return self.cleaned_data

    def save(self, *args, **kwargs):
        if not self.instance.pk:
            self.instance.user = self.user
        self.instance = super(TinylinkForm, self).save(*args, **kwargs)
        return validate_long_url(self.instance)

    class Meta:
        model = Tinylink
        fields = ('long_url', 'short_url')


class TinylinkAdminForm(forms.ModelForm):
    """
    Creates and updates long and short URL versions in the Django Admin.

    """
    def __init__(self, *args, **kwargs):
        """The Regex field validates the URL input."""
        super(TinylinkAdminForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:
            # Hide the short URL field to auto-generate a new instance.
            self.fields['short_url'].widget = forms.HiddenInput()
            self.fields['short_url'].required = False
        else:
            self.fields['short_url'] = forms.RegexField(
                regex=r'^[a-z0-9]+$',
                help_text=_("You can add a more readable short URL."),
                label=self.instance._meta.get_field('short_url').verbose_name,
            )
            self.fields['short_url'].error_messages['invalid'] = _(
                "Please use only small letters and digits.")

    def clean(self):
        self.cleaned_data = super(TinylinkAdminForm, self).clean()
        # If short URL is occupied throw out an error, or fail silent.
        try:
            twin = Tinylink.objects.get(
                short_url=self.cleaned_data.get('short_url'),
            )
        except Tinylink.DoesNotExist:
            slug = self.cleaned_data.get('short_url')
            while not slug or Tinylink.objects.filter(short_url=slug):
                slug = ''.join(
                    random.choice('abcdefghijkmnpqrstuvwxyz123456789')
                    for x in range(getattr(settings, 'TINYLINK_LENGTH', 6)))
            self.cleaned_data.update({'short_url': slug})
        else:
            if twin != self.instance:
                self._errors['short_url'] = ErrorList([_(
                    'This short url already exists. Please try another one.')])
        return self.cleaned_data

    class Meta:
        model = Tinylink
        fields = ('user', 'long_url', 'short_url')
