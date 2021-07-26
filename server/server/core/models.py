from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from server.assets.models import Asset

from .managers import StrategyQuerySet


class Strategy(models.Model):

    MOVING_AVERAGE_14D = "moving_average_14d"
    MOVING_AVERAGE_7D = "moving_average_7d"
    # TO DO
    # TO DO
    TYPE_CHOICES = [
        (MOVING_AVERAGE_14D, _("14 day moving average")),
        (MOVING_AVERAGE_7D, _("7 day moving average")),
    ]

    MIN_1 = "1Min"
    MIN_5 = "5Min"
    MIN_15 = "15Min"
    HOUR_1 = "1H"
    DAY_1 = "1D"
    TYPE_TIMEFRAME = [
        (MIN_1, _("1 minute")),
        (MIN_5, _("5 minute")),
        (MIN_15, _("15 minute")),
        (HOUR_1, _("1 hour")),
        (DAY_1, _("1 day")),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        related_name="+",
        on_delete=models.CASCADE,
    )
    type = models.CharField(
        verbose_name=_("type"),
        choices=TYPE_CHOICES,
        max_length=128,
    )
    asset = models.ForeignKey(
        Asset,
        verbose_name=_("asset"),
        related_name="+",
        on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField(_("start date"), blank=True, null=True)
    end_date = models.DateTimeField(_("end date"), blank=True, null=True)
    timeframe = models.CharField(
        verbose_name=_("timeframe"),
        choices=TYPE_TIMEFRAME,
        max_length=128,
        default=MIN_15,
    )
    trade_value = models.DecimalField(
        verbose_name=_("trade value"),
        max_digits=12,
        decimal_places=5,
    )
    stop_loss_amount = models.DecimalField(
        verbose_name=_("stop loss amount"),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True,
    )
    stop_loss_percentage = models.DecimalField(
        verbose_name=_("stop loss percentage"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    take_profit_amount = models.DecimalField(
        verbose_name=_("take profit amount"),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True,
    )
    take_profit_percentage = models.DecimalField(
        verbose_name=_("take profit percentage"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )

    objects = StrategyQuerySet.as_manager()

    class Meta:
        verbose_name = "strategy"
        verbose_name_plural = "strategies"

    def __str__(self):
        return f"{self.user.first_name} {self.type} {self.asset.symbol}"

    @property
    def is_active(self):
        time_now = timezone.now()
        return self.start_date <= time_now and self.end_date > time_now
