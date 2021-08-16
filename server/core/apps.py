"""Core app config."""
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _

from .signals import create_periodic_tasks


class CoreConfig(AppConfig):
    """Configuration for the core application."""

    name = "core"
    verbose_name = _("Core Config")

    def ready(self):
        post_migrate.connect(
            create_periodic_tasks,
            sender=self,
            dispatch_uid="core.signals.create_periodic_tasks",
        )
