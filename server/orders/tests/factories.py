import factory
from assets.tests.factories import AssetFactory
from django.utils import timezone
from factory.django import DjangoModelFactory
from orders.models import Order
from users.tests.factories import UserFactory


class OrderFactory(DjangoModelFactory):
    """Construct an order."""

    user = factory.SubFactory(UserFactory)
    id = factory.Faker("uuid4")
    client_order_id = factory.Faker("uuid4")
    created_at = factory.LazyFunction(timezone.now)
    asset_id = factory.SubFactory(AssetFactory)
    qty = 1000
    filled_qty = 1000
    type = (Order.MARKET,)
    side = (Order.BUY,)
    time_in_force = (Order.DAY,)
    status = Order.FILLED
    order_class = Order.SIMPLE

    class Meta:
        model = Order
