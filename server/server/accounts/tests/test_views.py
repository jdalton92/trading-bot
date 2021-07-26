from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from server.accounts.models import Account
from server.users.tests.factories import AdminFactory, UserFactory

from .factories import AccountFactory


class AccountViewTests(APITestCase):
    def setUp(self):
        self.admin = AdminFactory()
        self.user = UserFactory()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin.auth_token.key)
        self.account = AccountFactory(user=self.user)

    def test_list_accounts(self):
        """Admins can list accounts."""
        response = self.client.get(reverse("v1:accounts-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_account(self):
        """Admins and users can create accounts."""
        account_1 = {
            "id": "c74b4d35-ad27-4f57-9fc6-5c4ef106ef63",
            "account_blocked": False,
            "account_number": "ESS8FCSFK603",
            "buying_power": 0,
            "cash": 0,
            "created_at": timezone.now(),
            "currency": "USD",
            "daytrade_count": 0,
            "daytrading_buying_power": 0,
            "equity": 0,
            "initial_margin": 0,
            "last_equity": 0,
            "last_maintenance_margin": 0,
            "long_market_value": 0,
            "maintenance_margin": 0,
            "multiplier": 4,
            "pattern_day_trader": False,
            "portfolio_value": 0,
            "regt_buying_power": 0,
            "short_market_value": 0,
            "shorting_enabled": True,
            "sma": 0,
            "status": "ACTIVE",
            "trade_suspended_by_user": False,
            "trading_blocked": False,
            "transfers_blocked": False,
        }
        account_2 = {
            "id": "0c96a60c-e8a0-4deb-a0f1-e71d4b89dac5",
            "account_blocked": False,
            "account_number": "3UMZM893MOQM",
            "buying_power": 0,
            "cash": 0,
            "created_at": timezone.now(),
            "currency": "USD",
            "daytrade_count": 0,
            "daytrading_buying_power": 0,
            "equity": 0,
            "initial_margin": 0,
            "last_equity": 0,
            "last_maintenance_margin": 0,
            "long_market_value": 0,
            "maintenance_margin": 0,
            "multiplier": 4,
            "pattern_day_trader": False,
            "portfolio_value": 0,
            "regt_buying_power": 0,
            "short_market_value": 0,
            "shorting_enabled": True,
            "sma": 0,
            "status": "ACTIVE",
            "trade_suspended_by_user": False,
            "trading_blocked": False,
            "transfers_blocked": False,
        }

        # Admin create order
        response = self.client.post(reverse("v1:accounts-list"), account_1)
        account = Account.objects.filter(id=account_1["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(account.exists())

        # User create order
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.post(reverse("v1:accounts-list"), account_2)
        account = Account.objects.filter(id=account_2["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(account.exists())

    def test_partial_update_account(self):
        """Admins can patch accounts, users can patch their own account."""
        account_1 = {"status": Account.REJECTED}
        account_2 = {"status": Account.ONBOARDING}

        # Admin patch order
        response = self.client.patch(
            reverse("v1:accounts-detail", args=[self.account.pk]), account_1
        )
        self.account.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.account.status, account_1["status"])

        # User patch order
        response = self.client.patch(
            reverse("v1:accounts-detail", args=[self.account.pk]), account_2
        )
        self.account.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.account.status, account_2["status"])

    def test_admin_delete_account(self):
        """Admins can delete accounts."""
        response = self.client.delete(
            reverse("v1:accounts-detail", args=[self.account.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Account.objects.filter(pk=self.account.pk).exists())

    def test_user_delete_account(self):
        """Users can delete their own accounts."""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.auth_token.key)
        response = self.client.delete(
            reverse("v1:accounts-detail", args=[self.account.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Account.objects.filter(pk=self.account.pk).exists())

    def test_user_delete_account_invalid(self):
        """Users can not delete other user's accounts."""
        non_account_owner = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + non_account_owner.auth_token.key
        )
        response = self.client.delete(
            reverse("v1:accounts-detail", args=[self.account.pk])
        )

        # Returns HTTP 404 as other user's accounts are not visible to non admin
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Account.objects.filter(pk=self.account.pk).exists())
