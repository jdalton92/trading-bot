# Generated by Django 3.1.3 on 2020-12-22 12:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("assets", "0002_alter_group_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="Strategy",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("moving_average", "moving average")],
                        max_length=128,
                        verbose_name="type",
                    ),
                ),
                (
                    "start_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="start date"
                    ),
                ),
                (
                    "end_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="end date"
                    ),
                ),
                (
                    "trade_value",
                    models.DecimalField(
                        decimal_places=5, max_digits=12, verbose_name="trade value"
                    ),
                ),
                (
                    "stop_loss_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=5,
                        max_digits=12,
                        null=True,
                        verbose_name="stop loss amount",
                    ),
                ),
                (
                    "stop_loss_percentage",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=5,
                        null=True,
                        verbose_name="stop loss percentage",
                    ),
                ),
                (
                    "take_profit_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=5,
                        max_digits=12,
                        null=True,
                        verbose_name="take profit amount",
                    ),
                ),
                (
                    "take_profit_percentage",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=5,
                        null=True,
                        verbose_name="take profit percentage",
                    ),
                ),
                (
                    "asset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="assets.asset",
                        verbose_name="asset",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "strategy",
                "verbose_name_plural": "strategies",
            },
        ),
    ]
