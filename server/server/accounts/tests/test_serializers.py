from django.test import TestCase
from django.test.client import RequestFactory
from server.accounts.models import Account
from server.accounts.serializers import AccountSerializer
from server.users.tests.factories import AdminFactory, UserFactory

from .factories import AccountFactory


class AccountSerializerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = AdminFactory()
        cls.request = RequestFactory().get('/')
        cls.request.user = cls.admin

    def setUp(self):
        self.user = UserFactory()

    def test_view_account(self):
        """Account data is serialized correctly for users own account."""
        account = Account(
            id='2aa28199-1ff1-4b28-929b-51aaa3d7bdd7',
            user=self.user,
            account_blocked=False,
            account_number='PA24RIKIGB1U',
            buying_power=400000.01,
            cash=100000.01,
            created_at='2020-10-31T23:40:50.376107Z',
            currency='USD',
            daytrade_count=0,
            daytrading_buying_power=400000.01,
            equity=100000.01,
            initial_margin=0,
            last_equity=100000.01,
            last_maintenance_margin=0,
            long_market_value=0,
            maintenance_margin=0,
            multiplier=4,
            pattern_day_trader=False,
            portfolio_value=100000.01,
            regt_buying_power=200000.01,
            shorting_enabled=True,
            sma=0,
            status=Account.ACTIVE,
            trade_suspended_by_user=False,
            trading_blocked=False,
            transfers_blocked=False
        )

        data = AccountSerializer(
            account, context={'request': self.request}
        ).data

        self.assertEqual(data['id'], '2aa28199-1ff1-4b28-929b-51aaa3d7bdd7')
        self.assertEqual(
            data['user'],
            {
                "id": self.user.pk,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
            }
        )
        self.assertEqual(data['status'], Account.ACTIVE)
        self.assertFalse(data['account_blocked'])
        self.assertEqual(data['account_number'], 'PA24RIKIGB1U')
        self.assertEqual(float(data['buying_power']), 400000.01)
        self.assertEqual(float(data['cash']), 100000.01)
        self.assertEqual(data['currency'], 'USD')
        self.assertEqual(float(data['daytrade_count']), 0)
        self.assertEqual(float(data['daytrading_buying_power']), 400000.01)
        self.assertEqual(float(data['equity']), 100000.01)
        self.assertEqual(float(data['initial_margin']), 0)
        self.assertEqual(float(data['last_equity']), 100000.01)
        self.assertEqual(float(data['last_maintenance_margin']), 0)
        self.assertEqual(float(data['long_market_value']), 0)
        self.assertEqual(float(data['maintenance_margin']), 0)
        self.assertEqual(data['multiplier'], 4)
        self.assertFalse(data['pattern_day_trader'])
        self.assertEqual(float(data['portfolio_value']), 100000.01)
        self.assertEqual(float(data['regt_buying_power']), 200000.01)
        self.assertTrue(data['shorting_enabled'])
        self.assertEqual(float(data['sma']), 0)
        self.assertEqual(data['status'], Account.ACTIVE)
        self.assertFalse(data['trade_suspended_by_user'])
        self.assertFalse(data['trading_blocked'])
        self.assertFalse(data['transfers_blocked'])

    def test_create_account(self):
        """Account data is serialized correctly for users own account."""
        data = {
            'id': '2aa28199-1ff1-4b28-929b-51aaa3d7bdd7',
            'user': self.user.pk,
            'account_blocked': False,
            'account_number': 'PA24RIKIGB1U',
            'buying_power': 400000.01,
            'cash': 100000.01,
            'created_at': '2020-10-31T23:40:50.376107Z',
            'currency': 'USD',
            'daytrade_count': 0,
            'daytrading_buying_power': 400000.01,
            'equity': 100000.01,
            'initial_margin': 0,
            'last_equity': 100000.01,
            'last_maintenance_margin': 0,
            'long_market_value': 0,
            'maintenance_margin': 0,
            'multiplier': 4,
            'pattern_day_trader': False,
            'portfolio_value': 100000.01,
            'regt_buying_power': 200000.01,
            'short_market_value': 0,
            'shorting_enabled': True,
            'sma': 0,
            'status': 'ACTIVE',
            'trade_suspended_by_user': False,
            'trading_blocked': False,
            'transfers_blocked': False,
        }

        serializer = AccountSerializer(
            data=data,
            context={'request': self.request}
        )

        self.assertTrue(serializer.is_valid())
        account = serializer.save()

        self.assertEqual(data['id'], '2aa28199-1ff1-4b28-929b-51aaa3d7bdd7')
        self.assertEqual(self.user, account.user)
        self.assertEqual(data['status'], account.status)
        self.assertFalse(account.account_blocked)
        self.assertEqual(account.account_number, 'PA24RIKIGB1U')
        self.assertEqual(float(account.buying_power), 400000.01)
        self.assertEqual(float(account.cash), 100000.01)
        self.assertEqual(account.currency, 'USD')
        self.assertEqual(account.daytrade_count, 0)
        self.assertEqual(float(account.daytrading_buying_power), 400000.01)
        self.assertEqual(float(account.equity), 100000.01)
        self.assertEqual(account.initial_margin, 0)
        self.assertEqual(float(account.last_equity), 100000.01)
        self.assertEqual(account.last_maintenance_margin, 0)
        self.assertEqual(account.long_market_value, 0)
        self.assertEqual(account.maintenance_margin, 0)
        self.assertEqual(account.multiplier, 4)
        self.assertFalse(account.pattern_day_trader)
        self.assertEqual(float(account.portfolio_value), 100000.01)
        self.assertEqual(float(account.regt_buying_power), 200000.01)
        self.assertTrue(account.shorting_enabled)
        self.assertEqual(account.sma, 0)
        self.assertEqual(account.status, Account.ACTIVE)
        self.assertFalse(account.trade_suspended_by_user)
        self.assertFalse(account.trading_blocked)
        self.assertFalse(account.transfers_blocked)

    def test_update_account(self):
        """Order data is updated correctly for users."""
        account = AccountFactory(status='ACTIVE')
        serializer = AccountSerializer(
            account,
            data={'status': 'APPROVAL_PENDING'},
            partial=True,
            context={'request': self.request}
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        account.refresh_from_db()
        self.assertEqual(
            account.status,
            'APPROVAL_PENDING'
        )
