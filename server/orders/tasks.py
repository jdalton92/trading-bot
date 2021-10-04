import logging

from config import celery_app
from core.alpaca import TradeApiRest

from .models import Order
from .serializers import OrderCreateSerializer

logger = logging.getLogger(__name__)


def update_orders(user, orders=None):
    """Update db with historical orders placed from Alpaca account."""
    logger.info("Updating historical orders...")

    if orders is None:
        api = TradeApiRest()
        orders = api.get_orders(status="all", limit=500)

    existing_orders = [
        str(order_id) for order_id in Order.objects.all().values_list("pk", flat=True)
    ]
    new_orders = [
        order.__dict__["_raw"]
        for order in orders
        if str(order.__dict__["_raw"]["id"]) not in existing_orders
    ]
    serializer = OrderCreateSerializer(data=new_orders, many=True)
    serializer.is_valid(raise_exception=True)
    orders_to_create = [
        Order(**order_data, user=user) for order_data in serializer.validated_data
    ]
    Order.objects.bulk_create(objs=orders_to_create, ignore_conflicts=True)

    logger.info(f"Updates to orders: {len(new_orders)}")
