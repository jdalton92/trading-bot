from django.apps import AppConfig
from django.db.models.signals import post_save


class UsersConfig(AppConfig):

    name = "users"

    def ready(self):
        from .models import User
        from .signals import user_post_save

        post_save.connect(user_post_save, sender=User, dispatch_uid="user_post_save")
