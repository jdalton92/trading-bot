from api.users.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .factories import AdminFactory, UserFactory


class UserModelTests(TestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_login(self):
        """User can log in."""
        client = APIClient()
        client.login(username='testuser@tradingbot.com',
                     password='password123')
        self.assertIn(self.user, User.objects.all())


# class UserSerializerTests(TestCase):

#     def setUp(self):


# class UserViewTests(TestCase):

#     def setUp(self):
