from unittest.mock import patch

from django.test import TestCase


class CoreTaskTests(TestCase):
    @patch("server.core.alpaca.TradeApiRest")
    def setUp(self, mock_api):
        self.api = mock_api()

    def test_account_status(self):
        """Account is not blocked."""
        self.api._is_account_blocked.return_value = False
        self.assertFalse(self.api._is_account_blocked())
