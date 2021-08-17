import random

import factory
from assets.models import Asset, AssetClass, Bar, Exchange
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDecimal, FuzzyInteger


class ExchangeFactory(DjangoModelFactory):
    """Construct an exchange."""

    name = factory.Faker("catch_phrase")
    alt_name = factory.Faker("catch_phrase")
    is_active = True

    class Meta:
        model = Exchange


class AssetClassFactory(DjangoModelFactory):
    """Construct an asset class."""

    name = factory.Faker("catch_phrase")
    alt_name = factory.Faker("catch_phrase")
    is_active = True

    class Meta:
        model = AssetClass


class AssetFactory(DjangoModelFactory):
    """Construct an asset."""

    id = factory.Faker("uuid4")
    name = factory.Faker("catch_phrase")
    asset_class = factory.SubFactory(AssetClassFactory)
    easy_to_borrow = True
    exchange = factory.SubFactory(ExchangeFactory)
    marginable = True
    shortable = True
    status = Asset.ACTIVE
    symbol = factory.Faker("name")
    tradable = True

    class Meta:
        model = Asset


class BarFactory(DjangoModelFactory):
    """Construct bar data."""

    asset = factory.SubFactory(AssetFactory)
    t = FuzzyInteger(1, 2100000000)
    o = FuzzyDecimal(1, 1000)
    h = FuzzyDecimal(1, 1000)
    l = FuzzyDecimal(1, 1000)
    c = FuzzyDecimal(1, 1000)
    v = FuzzyInteger(1, 10000000)

    class Meta:
        model = Bar
