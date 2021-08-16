from assets.models import Asset
from core.models import Strategy
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import OrderQuerySet


class Order(models.Model):
    """An order placed by a user."""

    NEW = "new"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    DONE_FOR_DAY = "done_for_day"
    CANCELED = "canceled"
    EXPIRED = "expired"
    REPLACED = "replaced"
    PENDING_CANCEL = "pending_cancel"
    PENDING_REPLACE = "pending_replace"
    ACCEPTED = "accepted"
    PENDING_NEW = "pending_new"
    ACCEPTED_FOR_BIDDING = "accepted_for_bidding"
    STOPPED = "stopped"
    REJECTED = "rejected"
    SUSPENDED = "suspended"
    CALCULATED = "calculated"
    STATUS_CHOICES = [
        (NEW, _("new")),
        (PARTIALLY_FILLED, _("partially filled")),
        (FILLED, _("filled")),
        (DONE_FOR_DAY, _("done for day")),
        (CANCELED, _("canceled")),
        (EXPIRED, _("expired")),
        (REPLACED, _("replaced")),
        (PENDING_CANCEL, _("pending cancel")),
        (PENDING_REPLACE, _("pending replace")),
        (ACCEPTED, _("accepted")),
        (PENDING_NEW, _("pending new")),
        (ACCEPTED_FOR_BIDDING, _("accepted for bidding")),
        (STOPPED, _("stopped")),
        (REJECTED, _("rejected")),
        (SUSPENDED, _("suspended")),
        (CALCULATED, _("calculated")),
    ]

    BUY = "buy"
    SELL = "sell"
    SIDE_CHOICES = [
        (BUY, _("buy")),
        (SELL, _("sell")),
    ]

    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"
    TRAILING_STOP = "trailing_stop"
    TYPE_CHOICES = [
        (MARKET, _("market")),
        (LIMIT, _("limit")),
        (STOP, _("stop")),
        (STOP_LIMIT, _("stop limit")),
        (TRAILING_STOP, _("trailing stop")),
    ]

    DAY = "day"
    GTC = "gtc"
    OPG = "opg"
    CLS = "cls"
    IOC = "ioc"
    FOK = "fok"
    TIME_IN_FORCE_CHOICES = [
        (DAY, _("day")),
        (GTC, _("good till cancelled")),
        (OPG, _("order on open")),
        (CLS, _("order on close")),
        (IOC, _("immediate or cancel")),
        (FOK, _("fill or kill")),
    ]

    SIMPLE = "simple"
    BRACKET = "bracket"
    OCO = "oco"
    OTO = "oto"
    ORDER_CLASS_CHOICES = [
        (SIMPLE, _("simple")),
        (BRACKET, _("bracket")),
        (OCO, _("one cancels other")),
        (OTO, _("one triggers other")),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        related_name="+",
        on_delete=models.CASCADE,
    )
    strategy = models.ForeignKey(
        Strategy,
        verbose_name=_("strategy"),
        related_name="orders",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    # Use UUID returned from Alpaca api as primary key
    id = models.UUIDField(primary_key=True, editable=False, unique=True)
    client_order_id = models.UUIDField(editable=False, unique=True)
    created_at = models.DateTimeField(_("created"))
    updated_at = models.DateTimeField(_("modified"), blank=True, null=True)
    submitted_at = models.DateTimeField(_("submitted"), blank=True, null=True)
    filled_at = models.DateTimeField(_("filled"), blank=True, null=True)
    expired_at = models.DateTimeField(_("expired"), blank=True, null=True)
    canceled_at = models.DateTimeField(_("canceled"), blank=True, null=True)
    failed_at = models.DateTimeField(_("failed"), blank=True, null=True)
    replaced_at = models.DateTimeField(_("replaced"), blank=True, null=True)
    replaced_by = models.ForeignKey(
        "self",
        verbose_name=_("replaced by"),
        related_name="+",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    replaces = models.ForeignKey(
        "self",
        verbose_name=_("replaces"),
        related_name="+",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    asset_id = models.ForeignKey(
        Asset,
        verbose_name=_("asset id"),
        related_name="+",
        on_delete=models.CASCADE,
    )
    qty = models.DecimalField(
        verbose_name=_("quantity"),
        max_digits=12,
        decimal_places=5,
    )
    filled_qty = models.DecimalField(
        verbose_name=_("filled quantity"),
        max_digits=12,
        decimal_places=5,
    )
    type = models.CharField(
        verbose_name=_("type"),
        choices=TYPE_CHOICES,
        max_length=56,
    )
    side = models.CharField(
        verbose_name=_("side"),
        choices=SIDE_CHOICES,
        max_length=56,
    )
    time_in_force = models.CharField(
        verbose_name=_("time in force"),
        choices=TIME_IN_FORCE_CHOICES,
        max_length=56,
    )
    limit_price = models.DecimalField(
        verbose_name=_("limit price"),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True,
    )
    stop_price = models.DecimalField(
        verbose_name=_("stop price"),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True,
    )
    filled_avg_price = models.DecimalField(
        verbose_name=_("filled average price"),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True,
    )
    status = models.CharField(
        verbose_name=_("status"),
        choices=STATUS_CHOICES,
        max_length=56,
    )
    extended_hours = models.BooleanField(default=False)
    legs = models.ManyToManyField(
        "self",
        verbose_name=_("legs"),
        related_name="parent",
        symmetrical=False,
        blank=True,
    )
    trail_price = models.DecimalField(
        verbose_name=_("trail price"),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True,
    )
    trail_percentage = models.DecimalField(
        verbose_name=_("trail percentage"),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    hwm = models.DecimalField(
        verbose_name=_("hwm"), max_digits=12, decimal_places=5, blank=True, null=True
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"

    def __str__(self):
        return f"{self.side} {self.qty} {self.asset_id.symbol}"

    def clean(self):
        if self.strategy:
            if (
                self.asset_id.symbol != self.strategy.asset.symbol
                or self.symbol.symbol != self.strategy.asset.symbol
            ):
                raise ValidationError(
                    _("Strategy ``asset`` and order ``asset_id`` must be the " "same"),
                    code="invalid",
                )

    @property
    def symbol(self):
        return self.asset_id

    @property
    def asset_class(self):
        return self.asset_id.asset_class

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
