from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from server.orders.models import Strategy
from server.users.tests.factories import AdminFactory, UserFactory

from .factories import StrategyFactory


class StrategyQuerySetTests(TestCase):
    def setUp(self):
        self.admin = AdminFactory()
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.strategy = StrategyFactory(user=self.user_1)

    def test_strategy_visible_admins(self):
        """Admin can view all strategies."""
        visible = Strategy.objects.visible(self.admin)

        self.assertIn(self.strategy, visible)

    def test_strategy_visible_users(self):
        """User can only view their own strategies."""
        visible = Strategy.objects.visible(self.user_1)

        self.assertIn(self.strategy, visible)

    def test_strategy_visible_other_users(self):
        """User can not view others strategies."""
        visible = Strategy.objects.visible(self.user_2)

        self.assertNotIn(self.strategy, visible)

    def test_strategy_active(self):
        """Active strategies are returned."""
        inactive_strategy = StrategyFactory(
            start_date=timezone.now() - timedelta(days=2),
            end_date=timezone.now() - timedelta(days=1),
        )

        active_strategies = Strategy.objects.active()
        self.assertNotIn(inactive_strategy, active_strategies)
        self.assertIn(self.strategy, active_strategies)
