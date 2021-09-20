import uuid

from assets.tests.factories import AssetFactory
from core.tests.factories import StrategyFactory
from freezegun import freeze_time
from orders.models import Order
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from users.tests.factories import AdminFactory, UserFactory

from .factories import OrderFactory

time_now = "2021-01-30T05:25:22.831798Z"


@freeze_time(time_now)  # Freeze time for testing timedate fields
class OrderViewTests(APITestCase):
    def setUp(self):
        self.admin = AdminFactory()
        self.user = UserFactory()
        self.asset = AssetFactory(symbol="AAPL")
        self.strategy = StrategyFactory(asset=self.asset)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin.auth_token.key)
        self.order_1 = OrderFactory(
            user=self.user, strategy=self.strategy, asset_id=self.asset
        )
        self.order_2 = OrderFactory(
            user=self.user, strategy=self.strategy, asset_id=self.asset
        )
        self.order_3 = OrderFactory()
        self.order_4 = OrderFactory()

    def test_list_orders(self):
        """Admins can list orders."""
        response = self.client.get(reverse("v1:orders-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_create_order(self):
        """Admins and users can create orders."""
        uuid_1 = uuid.uuid4()
        uuid_2 = uuid.uuid4()
        uuid_3 = uuid.uuid4()
        uuid_4 = uuid.uuid4()
        order_1 = {
            "user": self.user.pk,
            "strategy": self.strategy.pk,
            "id": uuid_1,
            "client_order_id": uuid_2,
            "created_at": time_now,
            "updated_at": time_now,
            "submitted_at": time_now,
            "filled_at": time_now,
            "expired_at": time_now,
            "canceled_at": time_now,
            "failed_at": time_now,
            "replaced_at": time_now,
            "replaced_by": self.order_1.pk,
            "replaces": self.order_2.pk,
            "asset_id": self.asset.pk,
            "asset_class": self.asset.asset_class.name,
            "legs": [self.order_3.pk],
            "qty": 100,
            "filled_qty": 100,
            "type": Order.MARKET,
            "side": Order.BUY,
            "time_in_force": Order.DAY,
            "limit_price": 110.05,
            "stop_price": 90.05,
            "filled_avg_price": 100,
            "status": Order.FILLED,
            "extended_hours": True,
            "trail_price": 100,
            "trail_percent": 50.05,
            "hwm": 95.7,
        }
        order_2 = {
            "user": self.user.pk,
            "strategy": self.strategy.pk,
            "id": uuid_3,
            "client_order_id": uuid_4,
            "created_at": time_now,
            "updated_at": time_now,
            "submitted_at": time_now,
            "filled_at": time_now,
            "expired_at": time_now,
            "canceled_at": time_now,
            "failed_at": time_now,
            "replaced_at": time_now,
            "replaced_by": self.order_1.pk,
            "replaces": self.order_2.pk,
            "asset_id": self.asset.pk,
            "asset_class": self.asset.asset_class.name,
            "legs": [self.order_4.pk],
            "qty": 100,
            "filled_qty": 100,
            "type": Order.MARKET,
            "side": Order.BUY,
            "time_in_force": Order.DAY,
            "limit_price": 110.05,
            "stop_price": 90.05,
            "filled_avg_price": 100,
            "status": Order.FILLED,
            "extended_hours": True,
            "trail_price": 100,
            "trail_percent": 50.05,
            "hwm": 95.7,
        }

        # Admin create order
        response = self.client.post(reverse("v1:orders-list"), order_1)
        order = Order.objects.filter(client_order_id=order_1["client_order_id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(order.exists())

        # User create order
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post(reverse("v1:orders-list"), order_2)
        order = Order.objects.filter(client_order_id=order_2["client_order_id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(order.exists())

    def test_partial_update_order(self):
        """Admins and users can partially update orders."""
        order_1 = {"status": Order.PARTIALLY_FILLED}
        order_2 = {"status": Order.CANCELED}

        # Admin patch order
        response = self.client.patch(
            reverse("v1:orders-detail", args=[self.order_1.pk]), order_1
        )
        self.order_1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.order_1.status, order_1["status"])

        # User patch order
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.patch(
            reverse("v1:orders-detail", args=[self.order_2.pk]), order_2
        )
        self.order_2.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.order_2.status, order_2["status"])

    def test_admin_delete_order(self):
        """Admins can delete orders."""
        response = self.client.delete(
            reverse("v1:orders-detail", args=[self.order_1.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order_1.pk).exists())

    def test_user_delete_order(self):
        """Users can delete their own orders."""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.delete(
            reverse("v1:orders-detail", args=[self.order_1.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order_1.pk).exists())

    def test_user_delete_order_invalid(self):
        """Users can not delete other user's orders."""
        non_order_owner = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + non_order_owner.auth_token.key
        )
        response = self.client.delete(
            reverse("v1:orders-detail", args=[self.order_1.pk])
        )

        # Returns HTTP 404 as other user's orders are not visible to non admin
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Order.objects.filter(pk=self.order_1.pk).exists())
