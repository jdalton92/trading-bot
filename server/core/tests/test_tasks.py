from datetime import timedelta
from unittest.mock import patch

from core.tasks import run_strategies_for_users
from core.tests.factories import StrategyFactory
from django.test import TestCase
from django.utils import timezone
from users.tests.factories import UserFactory


class CoreTaskTests(TestCase):
    def setUp(self):
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.user_3 = UserFactory()
        self.strategy_1 = StrategyFactory(user=self.user_1)
        self.strategy_2 = StrategyFactory(user=self.user_2)
        self.inactive_strategy = StrategyFactory(
            user=self.user_3,
            start_date=timezone.now() - timedelta(days=7),
            end_date=timezone.now() - timedelta(days=5),
        )

    @patch("core.tasks.TradeApiRest")
    @patch("core.tasks.moving_average_strategy")
    def test_run_strategies_for_user(self, mock_moving_average_strategy, mock_api):
        """Moving average strategies that are active are run for users."""
        mock_api().is_market_open.return_value = True

        run_strategies_for_users()

        self.assertEqual(mock_moving_average_strategy.call_count, 2)
        mock_moving_average_strategy.assert_any_call(self.user_1)
        mock_moving_average_strategy.assert_any_call(self.user_2)

    def test_moving_average_strategy(self):
        """Active strategy creates and order."""
        # TODO
        pass
