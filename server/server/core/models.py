from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from server.assets.models import Asset

from .managers import StrategyQuerySet


class Strategy(models.Model):

    MOVING_AVERAGE = 'moving_average'
    # TO DO
    # TO DO
    TYPE_CHOICES = [
        (MOVING_AVERAGE, _('moving average')),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name='+',
        on_delete=models.CASCADE,
    )
    type = models.CharField(
        verbose_name=_('type'),
        choices=TYPE_CHOICES,
        max_length=128,
    )
    asset = models.ForeignKey(
        Asset,
        verbose_name=_('asset'),
        related_name='+',
        on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField(_('start date'), blank=True, null=True)
    end_date = models.DateTimeField(_('end date'), blank=True, null=True)
    trade_value = models.DecimalField(
        verbose_name=_('trade value'),
        max_digits=12,
        decimal_places=5,
    )
    stop_loss_amount = models.DecimalField(
        verbose_name=_('stop loss amount'),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True
    )
    stop_loss_percentage = models.DecimalField(
        verbose_name=_('stop loss percentage'),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )
    take_profit_amount = models.DecimalField(
        verbose_name=_('take profit amount'),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True
    )
    take_profit_percentage = models.DecimalField(
        verbose_name=_('take profit percentage'),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    objects = StrategyQuerySet.as_manager()

    class Meta:
        verbose_name = 'strategy'
        verbose_name_plural = 'strategies'

    def __str__(self):
        return f"{self.user.first_name} {self.type} {self.asset.symbol}"

    @property
    def is_active(self):
        time_now = timezone.now()
        return self.start_date <= time_now and self.end_date > time_now
