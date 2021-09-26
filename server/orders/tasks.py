import logging

from config import celery_app
from core.alpaca import TradeApiRest

from .models import Order
from .serializers import OrderCreateSerializer

logger = logging.getLogger(__name__)


def update_orders(orders=None):
    """Update db with historical orders placed from Alpaca account."""
    logger.info("Updating historical orders...")

    if orders is None:
        api = TradeApiRest()
        all_orders = api.get_orders(status="all", limit=500)

    existing_orders = [
        str(order_id) for order_id in Order.objects.all().values_list("pk", flat=True)
    ]
    new_orders = [
        order for order in all_orders if str(order["id"]) not in existing_orders
    ]
    bulk_add_orders(new_orders)

    logger.info(f"Updates to orders: {len(new_orders)}")


@celery_app.task(ignore_result=True)
def bulk_add_orders(orders):
    """
    Bulk create orders.

    :param orders(list): list of orders to be created
    """
    for order in orders:
        serializer = OrderCreateSerializer(data=order)
        # Fail silently for bulk add
        if serializer.is_valid():
            serializer.save()
