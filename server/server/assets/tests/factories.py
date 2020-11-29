import uuid

import factory
from factory.django import DjangoModelFactory
from server.assets.models import Asset, AssetClass, Exchange


class ExchangeFactory(DjangoModelFactory):
    """Construct an exchange."""

    name = factory.Faker('catch_phrase')
    alt_name = factory.Faker('catch_phrase')
    is_current = True

    class Meta:  # NOQA
        model = Exchange


class AssetClassFactory(DjangoModelFactory):
    """Construct an asset class."""

    name = factory.Faker('catch_phrase')
    alt_name = factory.Faker('catch_phrase')
    is_current = True

    class Meta:  # NOQA
        model = AssetClass


class AssetFactory(DjangoModelFactory):
    """Construct an asset."""

    id = uuid.uuid4()
    name = factory.Faker('catch_phrase')
    asset_class = AssetClassFactory()
    easy_to_borrow = True
    exchange = ExchangeFactory()
    marginable = True
    shortable = True
    status = Asset.ACTIVE
    symbol = factory.Faker('name')
    tradable = True

    class Meta:  # NOQA
        model = Asset
