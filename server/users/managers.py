from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Custom user manager."""

    def _create_user(self, email, password, **kwargs):
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        return user

    def create_user(self, email, password, **kwargs):
        """Create a new user."""
        user = self._create_user(email, password, **kwargs)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        """Create a new superuser."""
        user = self._create_user(email, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
