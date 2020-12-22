import uuid

import factory
from factory.django import DjangoModelFactory
from server.assets.models import Asset, AssetClass, Exchange


class ExchangeFactory(DjangoModelFactory):
    """Construct an exchange."""

    name = factory.Faker('catch_phrase')
    alt_name = factory.Faker('catch_phrase')
    is_active = True

    class Meta:
        model = Exchange


class AssetClassFactory(DjangoModelFactory):
    """Construct an asset class."""

    name = factory.Faker('catch_phrase')
    alt_name = factory.Faker('catch_phrase')
    is_active = True

    class Meta:
        model = AssetClass


class AssetFactory(DjangoModelFactory):
    """Construct an asset."""

    id = factory.Faker('uuid4')
    name = factory.Faker('catch_phrase')
    asset_class = factory.SubFactory(AssetClassFactory)
    easy_to_borrow = True
    exchange = factory.SubFactory(ExchangeFactory)
    marginable = True
    shortable = True
    status = Asset.ACTIVE
    symbol = factory.Faker('name')
    tradable = True

    class Meta:
        model = Asset
