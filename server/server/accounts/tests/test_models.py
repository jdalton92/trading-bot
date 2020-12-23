from django.test import TestCase
from server.accounts.models import Account
from server.users.tests.factories import UserFactory


class OrderTests(TestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_create_account(self):
        """An account object can be created."""
        account = Account(
            id='8dd89dc4-ac43-4ecd-88d0-75791d63621c',
            user=self.user,
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
        account.save()

        self.assertEqual(account.id, '8dd89dc4-ac43-4ecd-88d0-75791d63621c')
        self.assertEqual(account.user, self.user)
        self.assertFalse(account.account_blocked)
        self.assertEqual(account.account_number, 'PA24RIKIGB1U')
        self.assertEqual(account.buying_power, 400000)
        self.assertEqual(account.cash, 100000)
        self.assertEqual(account.currency, 'USD')
        self.assertEqual(account.daytrade_count, 0)
        self.assertEqual(account.daytrading_buying_power, 400000)
        self.assertEqual(account.equity, 100000)
        self.assertEqual(account.initial_margin, 0)
        self.assertEqual(account.last_equity, 100000)
        self.assertEqual(account.last_maintenance_margin, 20000)
        self.assertEqual(account.long_market_value, 50000)
        self.assertEqual(account.maintenance_margin, 10000)
        self.assertEqual(account.multiplier, 4)
        self.assertFalse(account.pattern_day_trader)
        self.assertEqual(account.portfolio_value, 60000)
        self.assertEqual(account.regt_buying_power, 5000)
        self.assertTrue(account.shorting_enabled)
        self.assertEqual(account.sma, 1000)
        self.assertEqual(account.status, Account.ACTIVE)
        self.assertFalse(account.trade_suspended_by_user)
        self.assertFalse(account.trading_blocked)
        self.assertFalse(account.transfers_blocked)
