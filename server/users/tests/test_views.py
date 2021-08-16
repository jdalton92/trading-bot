from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from users.models import User
from users.tests.factories import AdminFactory, UserFactory


class UserViewTests(APITestCase):
    def setUp(self):
        self.admin = AdminFactory()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin.auth_token.key)
        self.user = UserFactory(first_name="Name")
        self.data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@email.com",
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
        }

    def test_list_users(self):
        """User can view other users."""
        response = self.client.get(reverse("v1:users-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_user(self):
        """Admins can create new users."""
        response = self.client.post(reverse("v1:users-list"), self.data)
        user = User.objects.filter(email=self.data["email"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.exists())

        user = user.first()
        self.assertEqual(user.first_name, self.data["first_name"])
        self.assertEqual(user.last_name, self.data["last_name"])
        self.assertEqual(user.email, self.data["email"])
        self.assertEqual(user.is_active, self.data["is_active"])
        self.assertEqual(user.is_staff, self.data["is_staff"])
        self.assertEqual(user.is_superuser, self.data["is_superuser"])

    def test_create_user_invalid(self):
        """Users can not create new users."""
        user = UserFactory()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user.auth_token.key)
        response = self.client.post(reverse("v1:users-list"), self.data)
        user = User.objects.filter(email=self.data["email"])

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(user.exists())

    def test_user_partial_update(self):
        """Admins can patch user data."""
        data = {"first_name": "New Name"}

        response = self.client.patch(
            reverse("v1:users-detail", args=[self.user.pk]), data
        )
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.first_name, data["first_name"])

    def test_user_partial_update_invalid(self):
        """Users can not patch user data."""
        user = UserFactory()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user.auth_token.key)
        data = {"first_name": "New Name"}

        response = self.client.patch(
            reverse("v1:users-detail", args=[self.user.pk]), data
        )
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.user.first_name, "Name")

    def test_user_delete(self):
        """Admins can delete users."""
        response = self.client.delete(reverse("v1:users-detail", args=[self.user.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_user_delete_invalid(self):
        """Users can not delete users."""
        user = UserFactory()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user.auth_token.key)
        response = self.client.delete(reverse("v1:users-detail", args=[self.user.pk]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())
