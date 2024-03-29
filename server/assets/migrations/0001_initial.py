# Generated by Django 3.1.2 on 2020-11-07 04:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Exchange",
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
                ("name", models.CharField(max_length=255, verbose_name="name")),
                (
                    "alt_name",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="alt name"
                    ),
                ),
                ("is_current", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "exchange",
                "verbose_name_plural": "exchanges",
            },
        ),
        migrations.CreateModel(
            name="Asset",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                (
                    "asset_class",
                    models.CharField(max_length=255, verbose_name="asset class"),
                ),
                ("easy_to_borrow", models.BooleanField()),
                ("marginable", models.BooleanField()),
                ("shortable", models.BooleanField()),
                (
                    "status",
                    models.CharField(
                        choices=[("ACTIVE", "active"), ("INACTIVE", "inactive")],
                        max_length=56,
                        verbose_name="asset class",
                    ),
                ),
                (
                    "symbol",
                    models.CharField(max_length=56, unique=True, verbose_name="symbol"),
                ),
                ("tradeable", models.BooleanField()),
                (
                    "exchange",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="assets.exchange",
                        verbose_name="exchange",
                    ),
                ),
            ],
            options={
                "verbose_name": "asset",
                "verbose_name_plural": "assets",
            },
        ),
    ]
