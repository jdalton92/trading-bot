import uuid

import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
from server.assets.tests.factories import AssetFactory
from server.orders.models import Order, StopLoss, TakeProfit


class StopLossFactory(DjangoModelFactory):
    """Construct a stop loss."""

    stop_price = fuzzy.FuzzyDecimal(1, 5000)
    limit_price = fuzzy.FuzzyDecimal(1, 5000)

    class Meta:  # NOQA
        model = StopLoss


class TakeProfitFactory(DjangoModelFactory):
    """Construct a take profit."""

    limit_price = fuzzy.FuzzyDecimal(1, 5000)

    class Meta:  # NOQA
        model = TakeProfit


class OrderFactory(DjangoModelFactory):
    """Construct an order."""

    symbol = factory.SubFactory(AssetFactory)
    quantity = fuzzy.FuzzyDecimal(1, 100000),
    side = Order.BUY,
    type = Order.MARKET,
    time_in_force = Order.DAY,

    class Meta:  # NOQA
        model = Order
