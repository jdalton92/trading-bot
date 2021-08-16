from django.test import TestCase
from orders.models import Order
from users.tests.factories import AdminFactory, UserFactory

from .factories import OrderFactory


class OrderQuerySetTests(TestCase):
    def setUp(self):
        self.admin = AdminFactory()
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.order_1 = OrderFactory(user=self.user_1)

    def test_order_visible_admins(self):
        """Admin can view all orders."""
        visible = Order.objects.visible(self.admin)

        self.assertTrue(visible.filter(pk=self.order_1.pk))

    def test_order_visible_users(self):
        """User can only view their own orders."""
        visible = Order.objects.visible(self.user_1)

        self.assertTrue(visible.filter(pk=self.order_1.pk))

    def test_order_visible__other_users(self):
        """User can not view others orders."""
        visible = Order.objects.visible(self.user_2)

        self.assertFalse(visible.filter(pk=self.order_1.pk))
