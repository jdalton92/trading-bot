import random

import factory
import factory.fuzzy
from django.utils import timezone
from factory.django import DjangoModelFactory
from server.assets.tests.factories import AssetFactory
from server.core.models import Strategy
from server.users.tests.factories import UserFactory


class StrategyFactory(DjangoModelFactory):
    """Construct a strategy."""

    user = factory.SubFactory(UserFactory)
    type = Strategy.MOVING_AVERAGE_14D
    asset = factory.SubFactory(AssetFactory)
    start_date = factory.fuzzy.FuzzyDateTime(
        start_dt=timezone.now() - timezone.timedelta(days=6),
        end_dt=timezone.now() - timezone.timedelta(days=2),
    )
    end_date = factory.fuzzy.FuzzyDateTime(
        start_dt=timezone.now() + timezone.timedelta(days=2),
        end_dt=timezone.now() + timezone.timedelta(days=6),
    )
    trade_value = random.randint(1, 10000)

    class Meta:
        model = Strategy
