import random
import string

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from server.accounts.models import Account
from server.users.tests.factories import UserFactory


class AccountFactory(DjangoModelFactory):
    """Construct an account."""

    id = factory.Faker("uuid4")
    user = factory.SubFactory(UserFactory)
    account_blocked = False
    account_number = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=12)
    )
    buying_power = round(random.uniform(1.00, 100000.00), 2)
    cash = round(random.uniform(1.00, 100000.00), 2)
    created_at = timezone.now()
    currency = "USD"
    daytrade_count = random.randint(0, 100)
    daytrading_buying_power = round(random.uniform(1.00, 100000.00), 2)
    equity = round(random.uniform(1.00, 100000.00), 2)
    initial_margin = round(random.uniform(1.00, 100000.00), 2)
    last_equity = round(random.uniform(1.00, 100000.00), 2)
    last_maintenance_margin = round(random.uniform(1.00, 100000.00), 2)
    long_market_value = round(random.uniform(1.00, 100000.00), 2)
    maintenance_margin = round(random.uniform(1.00, 100000.00), 2)
    multiplier = 4
    pattern_day_trader = False
    portfolio_value = round(random.uniform(1.00, 100000.00), 2)
    regt_buying_power = round(random.uniform(1.00, 100000.00), 2)
    shorting_enabled = True
    sma = round(random.uniform(1.00, 100000.00), 2)
    status = Account.ACTIVE
    trade_suspended_by_user = False
    trading_blocked = False
    transfers_blocked = False

    class Meta:
        model = Account
