from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import CIEmailField
from django.db import models


class User(AbstractBaseUser):
    """A user of the app."""

    first_name = models.CharField("first name", max_length=100, blank=True)
    last_name = models.CharField("last name", max_length=100, blank=True)
    email = CIEmailField(
        "email",
        db_index=True,
        max_length=254,
        unique=True,
        help_text="User's main email address",
    )
    is_active = models.BooleanField("is active", default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
