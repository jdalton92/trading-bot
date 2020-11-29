from django.test import TestCase
from django.test.client import RequestFactory
from server.users.models import User
from server.users.serializers import UserSerializer


class ExchangeSerializerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = AdminFactory()
        cls.request = RequestFactory().get('/')
        cls.request.user = cls.admin

    def test_view_exchange(self):
        """Test exchange data is serialized correctly."""
        user = ExchangeFactory()
        data = ExchangeSerializer(user, context={'request': self.request}).data

        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['last_name'], 'User')
        self.assertEqual(data['email'], 'testuser@email.com')
        self.assertEqual(data['is_active'], True)
        self.assertEqual(data['is_staff'], False)
        self.assertEqual(data['is_superuser'], False)
        self.assertEqual(
            data['last_login'],
            self.datetime
        )
        self.assertEqual(
            data['date_joined'],
            self.datetime
        )
