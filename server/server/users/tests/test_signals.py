from unittest.mock import patch

from django.test import TestCase
from rest_framework.authtoken.models import Token
from server.users.tests.factories import UserFactory


class UserPostSaveTests(TestCase):

    @patch('server.users.signals.user_post_save')
    def test_create_user_post_save(self, user_post_save):
        """User post save signal is called when user instance is created."""
        UserFactory()
        self.assertTrue(user_post_save.called)

    def test_token_created(self):
        """Token is created for user when user instance is created."""
        user = UserFactory()
        self.assertEqual(Token.objects.all().count(), 1)
        self.assertEqual(Token.objects.filter(user=user).count(), 1)
