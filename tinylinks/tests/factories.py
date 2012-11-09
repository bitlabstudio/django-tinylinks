"""Utilities for creating test objects related to the ``django-tinylinks`` app."""
import factory

from tinylinks import models


class TinylinkFactory(factory.Factory):
    FACTORY_FOR = models.Tinylink

    long_url = "thisisalongURL"
    short_url = "vB7f5b"
