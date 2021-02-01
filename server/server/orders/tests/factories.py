import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from server.assets.tests.factories import AssetFactory
from server.orders.models import Order
from server.users.tests.factories import UserFactory


class OrderFactory(DjangoModelFactory):
    """Construct an order."""

    user = factory.SubFactory(UserFactory)
    id = factory.Faker('uuid4')
    client_order_id = factory.Faker('uuid4')
    created_at = factory.LazyFunction(timezone.now)
    asset_id = factory.SubFactory(AssetFactory)
    qty = 1000
    filled_qty = 1000
    type = Order.MARKET,
    side = Order.BUY,
    time_in_force = Order.DAY,
    status = Order.FILLED

    class Meta:
        model = Order
