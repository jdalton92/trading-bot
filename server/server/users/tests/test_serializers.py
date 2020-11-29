from datetime import datetime

import pytz
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone
from freezegun import freeze_time
from server.users.models import User
from server.users.serializers import UserSerializer
from server.users.tests.factories import AdminFactory, UserFactory


class UserSerializerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = AdminFactory()
        cls.request = RequestFactory().get('/')
        cls.request.user = cls.admin
        cls.datetime = '2020-11-29T00:00:00Z'

    def test_view_user(self):
        """Test user data is serialized correctly."""
        with freeze_time(self.datetime):
            user = UserFactory(
                first_name='Test',
                last_name='User',
                email='testuser@email.com',
                is_active=True,
                is_staff=False,
                is_superuser=False,
            )
            data = UserSerializer(user, context={'request': self.request}).data

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

    def test_user_profile_save(self):
        """Test user data is saved correctly."""
        with freeze_time(self.datetime):
            data = {
                "first_name": "Test",
                "last_name": "User",
                "email": "testuser@email.com",
            }

            serializer = UserSerializer(
                data=data, context={'request': self.request}
            )
            self.assertTrue(serializer.is_valid())
            user = serializer.save()

            self.assertEqual(User.objects.count(), 2)
            self.assertEqual(user.first_name, data['first_name'])
            self.assertEqual(user.last_name, data['last_name'])
            self.assertEqual(user.email, data['email'])
            self.assertTrue(user.is_active)
            self.assertFalse(user.is_staff)
            self.assertFalse(user.is_superuser)
            self.assertEqual(
                user.last_login,
                datetime(2020, 11, 29, 0, 0, 0, 0, tzinfo=pytz.UTC)
            )
            self.assertEqual(
                user.date_joined,
                datetime(2020, 11, 29, 0, 0, 0, 0, tzinfo=pytz.UTC)
            )