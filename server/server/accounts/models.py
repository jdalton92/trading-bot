from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import AccountQuerySet


class Account(models.Model):
    """Account information for a user of Alpaca trade api."""

    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"
    ONBOARDING = "ONBOARDING"
    SUBMISSION_FAILED = "SUBMISSION_FAILED"
    SUBMITTED = "SUBMITTED"
    ACCOUNT_UPDATED = "ACCOUNT_UPDATED"
    APPROVAL_PENDING = "APPROVAL_PENDING"
    STATUS_CHOICES = [
        (ACTIVE, _("active")),
        (REJECTED, _("rejected")),
        (ONBOARDING, _("onboarding")),
        (SUBMISSION_FAILED, _("submission failed")),
        (SUBMITTED, _("submitted")),
        (ACCOUNT_UPDATED, _("account updated")),
        (APPROVAL_PENDING, _("approval pending")),
    ]

    user = user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        related_name="+",
        on_delete=models.CASCADE,
    )
    account_blocked = models.BooleanField()
    account_number = models.CharField(
        verbose_name=_("account number"),
        max_length=56,
        unique=True,
    )
    buying_power = models.DecimalField(
        verbose_name=_("buying power"),
        max_digits=12,
        decimal_places=5,
    )
    cash = models.DecimalField(
        verbose_name=_("buying power"),
        max_digits=12,
        decimal_places=5,
    )
    created_at = models.DateTimeField(verbose_name=_("created"))
    currency = models.CharField(
        verbose_name=_("currency"), max_length=56, default="USD"
    )
    daytrade_count = models.PositiveIntegerField(default=0)
    daytrading_buying_power = models.DecimalField(
        verbose_name=_("daytrading buying power"),
        max_digits=12,
        decimal_places=5,
    )
    equity = models.DecimalField(
        verbose_name=_("equity"),
        max_digits=12,
        decimal_places=5,
    )
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
    )
    initial_margin = models.DecimalField(
        verbose_name=_("initial margin"),
        max_digits=12,
        decimal_places=5,
    )
    last_equity = models.DecimalField(
        verbose_name=_("last equity"),
        max_digits=12,
        decimal_places=5,
    )
    last_maintenance_margin = models.DecimalField(
        verbose_name=_("last maintenance margin"),
        max_digits=12,
        decimal_places=5,
    )
    long_market_value = models.DecimalField(
        verbose_name=_("long market value"),
        max_digits=12,
        decimal_places=5,
    )
    maintenance_margin = models.DecimalField(
        verbose_name=_("maintenance margin"),
        max_digits=12,
        decimal_places=5,
    )
    multiplier = models.PositiveIntegerField()
    pattern_day_trader = models.BooleanField()
    # Deprecated. Equivalent to equity field
    portfolio_value = models.DecimalField(
        verbose_name=_("portfolio value"),
        max_digits=12,
        decimal_places=5,
        default=0,
    )
    regt_buying_power = models.DecimalField(
        verbose_name=_("reg T buying power"),
        max_digits=12,
        decimal_places=5,
    )
    # Not used
    short_market_value = models.DecimalField(
        verbose_name=_("short market value"),
        max_digits=12,
        decimal_places=5,
        default=0,
    )
    shorting_enabled = models.BooleanField()
    sma = models.DecimalField(
        verbose_name=_("special memorandum account"),
        max_digits=12,
        decimal_places=5,
    )
    status = models.CharField(
        verbose_name=_("status"),
        choices=STATUS_CHOICES,
        max_length=56,
    )
    trade_suspended_by_user = models.BooleanField()
    trading_blocked = models.BooleanField()
    transfers_blocked = models.BooleanField()

    objects = AccountQuerySet.as_manager()

    class Meta:
        verbose_name = "account"
        verbose_name_plural = "accounts"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} Account"
