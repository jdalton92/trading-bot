from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from server.users.models import User
from server.users.tests.factories import AdminFactory, UserFactory


class UserViewTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.admin = AdminFactory()
        self.data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@email.com',
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
        }

    def login(self, user):
        """Login User."""
        self.client.force_authenticate(user)

    def test_list_users(self):
        """User can view other users."""
        self.login(self.user)
        response = self.client.get(reverse("v1:users-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_user(self):
        """Admins can create new users."""
        self.login(self.admin)
        response = self.client.post(reverse("v1:users-list"), self.data)
        user = User.objects.filter(email=self.data["email"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.exists())
        self.assertEqual(user.first_name, self.data['first_name'])
        self.assertEqual(user.last_name, self.data['last_name'])
        self.assertEqual(user.email, self.data['email'])
        self.assertEqual(user.is_active, self.data['is_active'])
        self.assertEqual(user.is_staff, self.data['is_staff'])
        self.assertEqual(user.is_superuser, self.data['is_superuser'])

    def test_user_partial_update(self):
        """Admins can patch user data."""
        self.login(self.admin)
        data = {"fist_name": "New Name"}

        response = self.client.patch(
            reverse("v1:users-detail", args=[self.user.pk]),
            data
        )
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, data["first_name"])

    def test_user_delete(self):
        """Admins can delete users."""
        self.login(self.admin)
        response = self.client.delete(
            reverse("v1:users-detail", args=[self.user.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
