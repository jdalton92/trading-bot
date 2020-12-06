import uuid

from django.contrib.postgres.fields import CICharField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Exchange(models.Model):
    """A exchange available via Alpaca."""

    name = models.CharField(
        verbose_name=_('name'),
        unique=True,
        max_length=256
    )
    alt_name = models.CharField(
        verbose_name=_('alt name'),
        max_length=256,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = 'exchange'
        verbose_name_plural = 'exchanges'

    def __str__(self):
        return f"{self.name}"


class AssetClass(models.Model):
    """An asset class."""

    name = models.CharField(
        verbose_name=_('name'),
        unique=True,
        max_length=256
    )
    alt_name = models.CharField(
        verbose_name=_('alt name'),
        max_length=256,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = 'asset class'
        verbose_name_plural = 'asset classes'

    def __str__(self):
        return f"{self.name}"


class Asset(models.Model):
    """A tradeable asset via Alpaca."""

    ACTIVE = 'active'
    INACTIVE = 'inactive'
    STATUS_CHOICES = [
        (ACTIVE, _('active')),
        (INACTIVE, _('inactive')),
    ]

    # Use UUID returned from Alpaca api as primary key
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4()
    )
    name = models.CharField(
        verbose_name=_('name'),
        max_length=256,
        blank=True,
        null=True,
    )
    asset_class = models.ForeignKey(
        AssetClass,
        verbose_name=_('asset class'),
        related_name='assets',
        on_delete=models.CASCADE,
    )
    easy_to_borrow = models.BooleanField()
    exchange = models.ForeignKey(
        Exchange,
        verbose_name=_('exchange'),
        related_name='assets',
        on_delete=models.CASCADE,
    )
    marginable = models.BooleanField()
    shortable = models.BooleanField()
    status = models.CharField(
        verbose_name=_('status'),
        choices=STATUS_CHOICES,
        max_length=56,
    )
    symbol = CICharField(
        verbose_name=_('symbol'),
        unique=True,
        max_length=56,
    )
    tradable = models.BooleanField()

    class Meta:
        verbose_name = _('asset')
        verbose_name_plural = _('assets')

    def __str__(self):
        return f"{self.name}"
