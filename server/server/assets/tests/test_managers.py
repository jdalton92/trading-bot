from django.test import TestCase
from server.assets.models import Bar
from server.users.tests.factories import AdminFactory, UserFactory

from .factories import AssetFactory, BarFactory


class BarQuerySetTests(TestCase):
    def setUp(self):
        self.admin = AdminFactory()
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.asset = AssetFactory()
        self.bar_1 = BarFactory(asset=self.asset)
        self.bar_2 = BarFactory(asset=self.asset)
        self.bar_3 = BarFactory()

    def test_bar_visible(self):
        """Correct bars are returned for a given asset id."""
        visible = Bar.objects.visible(self.asset.pk)

        self.assertIn(self.bar_1, visible)
        self.assertIn(self.bar_2, visible)
        self.assertNotIn(self.bar_3, visible)
