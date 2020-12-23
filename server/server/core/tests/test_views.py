from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from server.assets.tests.factories import AssetFactory
from server.core.models import Strategy
from server.users.tests.factories import AdminFactory, UserFactory

from .factories import StrategyFactory


class StrategyViewTests(APITestCase):

    def setUp(self):
        self.admin = AdminFactory()
        self.user = UserFactory()
        self.asset_1 = AssetFactory(symbol="AAPL")
        self.asset_2 = AssetFactory(symbol="TSLA")
        self.strategy = StrategyFactory(
            user=self.user,
            asset=self.asset_1
        )
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.admin.auth_token.key
        )

    def test_list_strategies(self):
        """Admins can list strategies."""
        response = self.client.get(reverse("v1:strategies-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_strategy(self):
        """Admins and users can create strategies."""
        strategy_1 = {
            "user": self.admin.pk,
            "type": Strategy.MOVING_AVERAGE_14D,
            "asset": self.asset_1.symbol,
            "start_date": timezone.now(),
            "end_date": timezone.now() + timedelta(days=2),
            "trade_value": 10000,
            "stop_loss_amount": 10,
        }
        strategy_2 = {
            "user": self.user.pk,
            "type": Strategy.MOVING_AVERAGE_14D,
            "asset": self.asset_2.symbol,
            "start_date": timezone.now(),
            "end_date": timezone.now() + timedelta(days=2),
            "trade_value": 10000,
            "stop_loss_amount": 10,
        }

        # Admin create order
        response = self.client.post(reverse("v1:strategies-list"), strategy_1)
        strategy = Strategy.objects.filter(
            user=self.admin,
            asset=self.asset_1
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(strategy.exists())

        # User create order
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key
        )
        response = self.client.post(reverse("v1:strategies-list"), strategy_2)
        strategy = Strategy.objects.filter(
            user=self.user,
            asset=self.asset_2
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(strategy.exists())

    def test_partial_update_strategy(self):
        """Admins and users can partially update strategies."""
        strategy_1 = {
            "asset": self.asset_1.symbol
        }
        strategy_2 = {
            "asset": self.asset_2.symbol
        }

        # Admin patch order
        response = self.client.patch(
            reverse("v1:strategies-detail", args=[self.strategy.pk]),
            strategy_1
        )
        self.strategy.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.strategy.asset.symbol, strategy_1["asset"])

        # User patch order
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key
        )
        response = self.client.patch(
            reverse("v1:strategies-detail", args=[self.strategy.pk]),
            strategy_2
        )
        self.strategy.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.strategy.asset.symbol, strategy_2["asset"])

    def test_admin_delete_strategy(self):
        """Admins can delete strategies."""
        response = self.client.delete(
            reverse("v1:strategies-detail", args=[self.strategy.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Strategy.objects.filter(pk=self.strategy.pk).exists()
        )

    def test_user_delete_strategy(self):
        """Users can delete their own strategies."""
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key
        )
        response = self.client.delete(
            reverse("v1:strategies-detail", args=[self.strategy.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Strategy.objects.filter(pk=self.strategy.pk).exists()
        )

    def test_user_delete_strategy_invalid(self):
        """Users can not delete other user's strategies."""
        non_strategy_owner = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + non_strategy_owner.auth_token.key
        )
        response = self.client.delete(
            reverse("v1:strategies-detail", args=[self.strategy.pk])
        )

        # Returns HTTP 404 as other user's strategies are not visible to users
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(
            Strategy.objects.filter(pk=self.strategy.pk).exists()
        )
