from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from rest_framework.test import APIClient
from server.users.models import User

from .factories import UserFactory

time_now = timezone.now()


@freeze_time(time_now)  # Freeze time for testing timedate fields
class UserModelTests(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()

    def test_login(self):
        """User can log in."""
        self.client.login(
            username='testuser@tradingbot.com', password='password123'
        )
        self.assertIn(self.user, User.objects.all())

    def test_create_user(self):
        """User instance can be created."""
        user = UserFactory(
            first_name='Test',
            last_name='User',
            email='testuser@email.com',
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )
        self.assertIn(user, User.objects.all())
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.email, 'testuser@email.com')
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.last_login, time_now)
        self.assertEqual(user.date_joined, time_now)
