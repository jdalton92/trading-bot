from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from server.assets.models import Asset
from server.orders.models import Order


class Strategy(models.Model):

    MOVING_AVERAGE = 'moving_average'
    # TO DO
    # TO DO
    STRATEGY_CHOICES = [
        (MOVING_AVERAGE, _('moving average')),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        related_name='+',
        on_delete=models.CASCADE,
    )
    strategy = models.CharField(
        verbose_name=_('status'),
        choices=STRATEGY_CHOICES,
        max_length=128,
    )
    asset = models.ForeignKey(
        Asset,
        verbose_name=_('asset'),
        related_name='+',
        on_delete=models.CASCADE,
    )
    orders = models.ForeignKey(
        Order,
        verbose_name=_('orders'),
        related_name='+',
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=False)
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

    class Meta:
        verbose_name = 'strategy'
        verbose_name_plural = 'strategies'

    def __str__(self):
        return f"{self.user.first_name} {self.strategy} {self.asset.symbol}"
