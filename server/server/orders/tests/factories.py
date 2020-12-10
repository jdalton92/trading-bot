import random
import uuid

import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
from server.assets.tests.factories import AssetFactory
from server.orders.models import Order, StopLoss, TakeProfit


class StopLossFactory(DjangoModelFactory):
    """Construct a stop loss."""

    stop_price = round(random.uniform(1.00, 5000.00), 2)
    limit_price = round(random.uniform(1.00, 5000.00), 2)

    class Meta:  # NOQA
        model = StopLoss


class TakeProfitFactory(DjangoModelFactory):
    """Construct a take profit."""

    limit_price = round(random.uniform(1.00, 5000.00), 2)

    class Meta:  # NOQA
        model = TakeProfit


class OrderFactory(DjangoModelFactory):
    """Construct an order."""

    symbol = factory.SubFactory(AssetFactory)
    quantity = round(random.uniform(1.00, 100000.00), 2)
    side = Order.BUY,
    type = Order.MARKET,
    time_in_force = Order.DAY,
    client_order_id = factory.Faker('uuid4')

    class Meta:  # NOQA
        model = Order
