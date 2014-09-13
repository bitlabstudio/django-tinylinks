"""
Utilities for creating test objects related to the ``django-tinylinks`` app.

"""
import factory

from django_libs.tests.factories import UserFactory

from tinylinks import models


class TinylinkFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Tinylink

    user = factory.SubFactory(UserFactory)
    long_url = "http://www.example.com/thisisalongURL"
    short_url = "vB7f5b"
