import uuid

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from server.assets.tests.factories import AssetFactory
from server.core.tests.factories import StrategyFactory
from server.orders.models import Order
from server.users.tests.factories import AdminFactory, UserFactory

from .factories import OrderFactory


class OrderViewTests(APITestCase):

    def setUp(self):
        self.admin = AdminFactory()
        self.user = UserFactory()
        self.asset = AssetFactory(symbol="AAPL")
        self.strategy = StrategyFactory(
            asset=self.asset
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.admin.auth_token.key
        )
        self.stop_loss = {
            "stop_price": 100.50,
            "limit_price": 110.30
        }
        self.take_profit = {
            "limit_price": 110.30
        }
        self.order_1 = OrderFactory(
            user=self.user,
            strategy=self.strategy,
            symbol=self.asset
        )
        self.order_2 = OrderFactory(
            user=self.user,
            strategy=self.strategy,
            symbol=self.asset
        )

    def test_list_orders(self):
        """Admins can list orders."""
        response = self.client.get(reverse("v1:orders-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_order(self):
        """Admins and users can create orders."""
        order_1 = {
            "user": self.user.pk,
            "strategy": self.strategy.pk,
            "status": "open",
            "symbol": "AAPL",
            "quantity": 100.05,
            "side": "buy",
            "type": "market",
            "time_in_force": "day",
            "client_order_id": str(uuid.uuid4())
        }
        order_2 = {
            "user": self.user.pk,
            "strategy": self.strategy.pk,
            "status": "open",
            "symbol": "AAPL",
            "quantity": 100.05,
            "side": "sell",
            "type": "market",
            "time_in_force": "day",
            "client_order_id": str(uuid.uuid4())
        }

        # Admin create order
        response = self.client.post(reverse("v1:orders-list"), order_1)
        order = Order.objects.filter(client_order_id=order_1["client_order_id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(order.exists())

        # User create order
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key
        )
        response = self.client.post(reverse("v1:orders-list"), order_2)
        order = Order.objects.filter(client_order_id=order_2["client_order_id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(order.exists())

    def test_partial_update_order(self):
        """Admins and users can partially update orders."""
        order_1 = {
            "status": Order.CLOSED
        }
        order_2 = {
            "status": Order.OPEN
        }

        # Admin patch order
        response = self.client.patch(
            reverse("v1:orders-detail", args=[self.order_1.pk]),
            order_1
        )
        self.order_1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.order_1.status, order_1["status"])

        # User patch order
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key
        )
        response = self.client.patch(
            reverse("v1:orders-detail", args=[self.order_2.pk]),
            order_2
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
        self.assertFalse(
            Order.objects.filter(pk=self.order_1.pk).exists()
        )

    def test_user_delete_order(self):
        """Users can delete their own orders."""
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key
        )
        response = self.client.delete(
            reverse("v1:orders-detail", args=[self.order_1.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Order.objects.filter(pk=self.order_1.pk).exists()
        )

    def test_user_delete_order_invalid(self):
        """Users can not delete other user's orders."""
        non_order_owner = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + non_order_owner.auth_token.key
        )
        response = self.client.delete(
            reverse("v1:orders-detail", args=[self.order_1.pk])
        )

        # Returns HTTP 404 as other user's orders are not visible to non admin
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(
            Order.objects.filter(pk=self.order_1.pk).exists()
        )
