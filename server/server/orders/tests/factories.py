import random
import uuid

import factory
from factory.django import DjangoModelFactory
from server.assets.tests.factories import AssetFactory
from server.core.tests.factories import StrategyFactory
from server.orders.models import Order
from server.users.tests.factories import UserFactory


class OrderFactory(DjangoModelFactory):
    """Construct an order."""

    user = factory.SubFactory(UserFactory)
    strategy = factory.SubFactory(StrategyFactory)
    symbol = factory.SubFactory(AssetFactory)
    quantity = round(random.uniform(1.00, 100000.00), 2)
    side = Order.BUY,
    type = Order.MARKET,
    time_in_force = Order.DAY,
    client_order_id = factory.Faker('uuid4')

    class Meta:
        model = Order
