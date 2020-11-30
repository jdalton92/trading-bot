from datetime import datetime

import pytz
from django.test import TestCase
from django.test.client import RequestFactory
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
        """User data is serialized correctly."""
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

            self.assertEqual(data['first_name'], user.first_name)
            self.assertEqual(data['last_name'], user.last_name)
            self.assertEqual(data['email'], user.email)
            self.assetTrue(data['is_active'])
            self.assertFalse(data['is_staff'])
            self.assertFalse(data['is_superuser'])
            self.assertEqual(
                data['last_login'],
                self.datetime
            )
            self.assertEqual(
                data['date_joined'],
                self.datetime
            )

    def test_create_user(self):
        """User data is saved correctly."""
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

    def test_update_user(self):
        """User data is updated correctly."""
        user = UserFactory(first_name='Old Name')
        serializer = UserSerializer(
            user,
            data={'first_name': 'New Name'},
            partial=True,
            context={'request': self.request}
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        user.refresh_from_db()
        self.assertEqual(user.first_name, 'New Name')
