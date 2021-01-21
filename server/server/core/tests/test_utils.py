from django.test import TestCase
from server.core.alpaca import TradeApiRest


class CoreTaskTests(TestCase):

    def setUp(self):
        self.api = TradeApiRest()

    def test_account_status(self):
        """Account is not blocked."""
        self.assertFalse(self.api._is_account_blocked())
