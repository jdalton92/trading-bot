from datetime import timedelta

from assets.tests.factories import AssetFactory
from core.models import Strategy
from core.serializers import StrategyCreateSerializer, StrategySerializer
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone
from freezegun import freeze_time
from orders.tests.factories import OrderFactory
from users.serializers import UserSerializer
from users.tests.factories import AdminFactory, UserFactory

from .factories import StrategyFactory


@freeze_time("2020-12-17T06:29:12.853922Z")
class StrategySerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = AdminFactory()
        cls.request = RequestFactory().get("/")
        cls.request.user = cls.admin

    def setUp(self):
        self.user = UserFactory()
        self.asset = AssetFactory(symbol="AAPL")
        self.strategy = StrategyFactory(asset=self.asset)
        self.order = OrderFactory(strategy=self.strategy, asset_id=self.asset)

    def test_view_strategy(self):
        """Strategy data is serialized correctly."""
        strategy = StrategyFactory(
            start_date=timezone.now(), end_date=timezone.now() + timedelta(days=2)
        )
        data = StrategySerializer(strategy, context={"request": self.request}).data

        self.assertEqual(
            data["user"],
            UserSerializer(
                strategy.user, fields=("id", "first_name", "last_name")
            ).data,
        )
        self.assertEqual(data["type"], strategy.type)
        self.assertEqual(data["asset"], strategy.asset.symbol)
        self.assertEqual(data["start_date"], "2020-12-17T06:29:12.853922Z")
        self.assertEqual(data["end_date"], "2020-12-19T06:29:12.853922Z")
        self.assertEqual(float(data["trade_value"]), strategy.trade_value)
        self.assertEqual(data["timeframe"], Strategy.MIN_15)

    def test_create_strategy(self):
        """Strategy data is saved correctly."""
        data = {
            "user": self.user.pk,
            "type": Strategy.MOVING_AVERAGE_14D,
            "asset": self.asset.symbol,
            "start_date": timezone.now(),
            "end_date": timezone.now() + timedelta(days=2),
            "trade_value": 10000,
            "timeframe": Strategy.MIN_1,
        }
        serializer = StrategyCreateSerializer(
            data=data, context={"request": self.request}
        )

        self.assertTrue(serializer.is_valid())
        strategy = serializer.save()

        self.assertEqual(self.user, strategy.user)
        self.assertEqual(data["type"], strategy.type)
        self.assertEqual(data["asset"], strategy.asset.symbol)
        self.assertEqual(data["start_date"], strategy.start_date)
        self.assertEqual(data["end_date"], strategy.end_date)
        self.assertEqual(float(data["trade_value"]), strategy.trade_value)
        self.assertEqual(data["timeframe"], strategy.timeframe)

    def test_create_strategy_invalid_stop_loss(self):
        """
        Validation error is raised when using bot stop lost percentage and
        amount.
        """
        data = {
            "user": self.user.pk,
            "type": Strategy.MOVING_AVERAGE_14D,
            "asset": self.asset.symbol,
            "start_date": timezone.now(),
            "end_date": timezone.now() + timedelta(days=2),
            "trade_value": 10000,
            "stop_loss_amount": 10,
            "stop_loss_percentage": 10,
        }
        serializer = StrategyCreateSerializer(
            data=data, context={"request": self.request}
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["stop_loss_amount"][0]),
            "Enter either `stop_loss_amount` or `stop_loss_percentage`, but not"
            " both",
        )
        self.assertEqual(
            str(serializer.errors["stop_loss_percentage"][0]),
            "Enter either `stop_loss_amount` or `stop_loss_percentage`, but not"
            " both",
        )

    def test_create_strategy_invalid_take_profit(self):
        """
        Validation error is raised when using bot take profit percentage and
        amount.
        """
        data = {
            "user": self.user.pk,
            "type": Strategy.MOVING_AVERAGE_14D,
            "asset": self.asset.symbol,
            "start_date": timezone.now(),
            "end_date": timezone.now() + timedelta(days=2),
            "trade_value": 10000,
            "take_profit_amount": 10,
            "take_profit_percentage": 10,
        }
        serializer = StrategyCreateSerializer(
            data=data, context={"request": self.request}
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["take_profit_amount"][0]),
            "Enter either `take_profit_amount` or `take_profit_percentage`, but"
            " not both",
        )
        self.assertEqual(
            str(serializer.errors["take_profit_percentage"][0]),
            "Enter either `take_profit_amount` or `take_profit_percentage`, but"
            " not both",
        )

    def test_update_strategy(self):
        """Strategy data is updated correctly."""
        serializer = StrategyCreateSerializer(
            self.strategy,
            data={"type": Strategy.MOVING_AVERAGE_7D},
            partial=True,
            context={"request": self.request},
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.strategy.refresh_from_db()
        self.assertEqual(self.strategy.type, Strategy.MOVING_AVERAGE_7D)
