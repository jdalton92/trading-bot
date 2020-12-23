import uuid

from django.test import TestCase
from server.accounts.models import Account
from server.users.tests.factories import AdminFactory, UserFactory


class AccountQuerySetTests(TestCase):

    def setUp(self):
        self.admin = AdminFactory()
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.account_1 = Account.objects.create(
            id=uuid.uuid4(),
            user=self.user_1,
            account_blocked=False,
            account_number='PA24RIKIGB1U',
            buying_power=400000,
            cash=100000,
            created_at='2020-10-31T23:40:50.376107Z',
            currency='USD',
            daytrade_count=0,
            daytrading_buying_power=400000,
            equity=100000,
            initial_margin=0,
            last_equity=100000,
            last_maintenance_margin=20000,
            long_market_value=50000,
            maintenance_margin=10000,
            multiplier=4,
            pattern_day_trader=False,
            portfolio_value=60000,
            regt_buying_power=5000,
            shorting_enabled=True,
            sma=1000,
            status=Account.ACTIVE,
            trade_suspended_by_user=False,
            trading_blocked=False,
            transfers_blocked=False
        )

    def test_account_visible_admins(self):
        """Admin can view all accounts."""
        visible = Account.objects.visible(self.admin)

        self.assertIn(self.account_1, visible)

    def test_account_visible_users(self):
        """User can only view their own accounts."""
        visible = Account.objects.visible(self.user_1)

        self.assertIn(self.account_1, visible)

    def test_account_visible__other_users(self):
        """User can not view others accounts."""
        visible = Account.objects.visible(self.user_2)

        self.assertNotIn(self.account_1, visible)
