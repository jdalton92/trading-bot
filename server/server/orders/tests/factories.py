import random
import uuid
from decimal import Decimal

import factory
from factory.django import DjangoModelFactory
from server.assets.tests.factories import AssetFactory
from server.orders.models import Order
from server.users.tests.factories import UserFactory


class OrderFactory(DjangoModelFactory):
    """Construct an order."""

    user = factory.SubFactory(UserFactory)
    symbol = factory.SubFactory(AssetFactory)
    quantity = Decimal(random.uniform(1.00, 100000.00))
    side = Order.BUY,
    type = Order.MARKET,
    time_in_force = Order.DAY,
    client_order_id = factory.Faker('uuid4')

    class Meta:
        model = Order
