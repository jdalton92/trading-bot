from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from server.users.tests.factories import AdminFactory, UserFactory


class UserTests(APITestCase):

    @ classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.admin = AdminFactory()
        cls.data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@email.com',
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
        }

    def setUp(self):
        self.user.refresh_from_db()
        self.admin.refresh_from_db()

    def login(self, user):
        """Login User."""
        self.client.force_authenticate(user)

    def test_list(self):
        """User can view other users."""
        self.login(self.user)
        response = self.client.get(reverse("v1:users-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
