from django.db import models
from model_utils.models import TimeStampedModel


class StopLoss(models.Model):
    """Stop loss model for advanced orders."""

    stop_price = models.DecimalField(
        verbose_name=_('stop price'),
        max_digits=12,
        decimal_places=5
    )
   limit_price = models.DecimalField(
        verbose_name=_('limit price'),
        max_digits=12,
        decimal_places=5
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'stop loss'
        verbose_name_plural = 'stop losses'

    def __str__(self):
        return f"{self.stop_price}"


class TakeProfit(models.Model):
    """Take profit model for advanced orders."""

    limit_price = models.DecimalField(
        verbose_name=_('limit price'),
        max_digits=12,
        decimal_places=5
    )

    class Meta:
        verbose_name = 'take profit'
        verbose_name_plural = 'take profits'

    def __str__(self):
        return f"{self.limit_price}"


class Order(TimeStampedModel):
    """An order placed by a user."""

    OPEN = 'open'
    CLOSED = 'closed'
    STATUS_CHOICES = [
        (OPEN, _('open')),
        (CLOSED, _('closed')),
    ]

    BUY = 'buy'
    SELL = 'sell'
    SIDE_CHOICES = [
        (BUY, _('buy')),
        (SELL, _('sell')),
    ]

    MARKET = 'market'
    LIMIT = 'limit'
    STOP = 'stop'
    STOP_LIMIT = 'stop_limit'
    TRAILING_STOP = 'trailing_stop'
    TYPE_CHOICES =[
        (MARKET, _('market')),
        (LIMIT, _('limit')),
        (STOP, _('stop')),
        (STOP_LIMIT, _('stop limit')),
        (TRAILING_STOP, _('trailing stop')),
    ]

    DAY = 'day'
    GTC = 'gtc'
    OPG = 'opg'
    CLS = 'cls'
    IOC = 'ioc'
    FOK = 'fok'
    TIME_IN_FORCE_CHOICES = [
        (DAY, _('day')),
        (GTC, _('good till cancelled')),
        (OPG, _('order on open')),
        (CLS, _('order on close')),
        (IOC, _('immediate or cancel')),
        (FOK, _('fill or kill')),
    ]

    SIMPLE = 'simple'
    BRACKET = 'bracket'
    OCO = 'oco'
    OTO = 'oto'
    ORDER_CLASS_CHOICES = [
        (SIMPLE, _('simple')),
        (BRACKET, _('bracket')),
        (OCO, _('one cancels other')),
        (OTO, _('one triggers other')),
    ]

    status = models.CharField(
        verbose_name=_('status'),
        choices=STATUS_CHOICES,
        max_length=56,
    )
    symbol = models.ForeignKey(
        Asset,
        verbose_name=_('symbols'),
        related_name='trades',
        on_delete=models.CASCADE,
    )
    quantity = models.DecimalField(
        verbose_name=_('quantity'),
        max_digits=12,
        decimal_places=5,
    )
    side = models.CharField(
        verbose_name=_('side'),
        choices=SIDE_CHOICES,
        max_length=56,
    )
    type = models.CharField(
        verbose_name=_('side'),
        choices=TYPE_CHOICES,
        max_length=56,
    )
    time_in_force = models.CharField(
        verbose_name=_('time in force'),
        choices=TIME_IN_FORCE_CHOICES,
        max_length=56,
    )
    limit_price = models.DecimalField(
        verbose_name=_('limit price'),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True
    )
    stop_price = models.DecimalField(
        verbose_name=_('stop price'),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True
    )
    trail_price = models.DecimalField(
        verbose_name=_('trail price'),
        max_digits=12,
        decimal_places=5,
        blank=True,
        null=True
    )
    trail_percentage = models.DecimalField(
        verbose_name=_('trail percentage'),
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )
    extended_hours = models.BooleanField(default=False)
    client_order_id = models.UUIDField(
        editable=False,
        unique=True,
    )
    order_class = models.CharField(
        verbose_name=_('order class'),
        choices=ORDER_CLASS_CHOICES,
        max_length=56,
    )
    take_profit = models.ForeignKey(
        TakeProfit,
        verbose_name=_('take profit'),
        related_name='+',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    stop_loss = models.ForeignKey(
        StopLoss,
        verbose_name=_('stop loss'),
        related_name='+',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f"{self.side} {self.quantity} {self.symbol.symbol}"