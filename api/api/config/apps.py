"""Core app config."""
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _

from .signals import create_periodic_tasks


class CoreAppConfig(AppConfig):
    """Configuration for the core application."""

    name = 'api.config'
    verbose_name = _('Config)

    def ready(self):
        post_migrate.connect(
            create_periodic_tasks, sender=self,
            dispatch_uid="api.core.signals.create_periodic_tasks"
        )
