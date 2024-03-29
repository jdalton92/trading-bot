from django.contrib.auth.models import AbstractBaseUser, Group, PermissionsMixin
from django.contrib.postgres.fields import CIEmailField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """A user of the app."""

    first_name = models.CharField(_("first name"), max_length=100, blank=True)
    last_name = models.CharField(_("last name"), max_length=100, blank=True)
    email = CIEmailField(
        _("email"),
        db_index=True,
        max_length=254,
        unique=True,
        help_text="User's main email address",
    )
    groups = models.ManyToManyField(Group, blank=True)
    is_active = models.BooleanField(_("is active"), default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(_("last login"), default=timezone.now)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}"

    @property
    def is_admin(self):
        return self.is_staff
