# Generated by Django 3.1.3 on 2021-01-28 07:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assets', '0002_alter_group_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(editable=False,
                                        primary_key=True, serialize=False, unique=True)),
                ('client_order_id', models.UUIDField(editable=False, unique=True)),
                ('created_at', models.DateTimeField(verbose_name='created')),
                ('updated_at', models.DateTimeField(
                    blank=True, null=True, verbose_name='modified')),
                ('submitted_at', models.DateTimeField(
                    blank=True, null=True, verbose_name='submitted')),
                ('filled_at', models.DateTimeField(
                    blank=True, null=True, verbose_name='filled')),
                ('expired_at', models.DateTimeField(
                    blank=True, null=True, verbose_name='expired')),
                ('canceled_at', models.DateTimeField(
                    blank=True, null=True, verbose_name='canceled')),
                ('failed_at', models.DateTimeField(
                    blank=True, null=True, verbose_name='failed')),
                ('replaced_at', models.DateTimeField(
                    blank=True, null=True, verbose_name='replaced')),
                ('qty', models.DecimalField(decimal_places=5,
                                            max_digits=12, verbose_name='quantity')),
                ('filled_qty', models.DecimalField(decimal_places=5,
                                                   max_digits=12, verbose_name='filled quantity')),
                ('type', models.CharField(choices=[('market', 'market'), ('limit', 'limit'), ('stop', 'stop'), (
                    'stop_limit', 'stop limit'), ('trailing_stop', 'trailing stop')], max_length=56, verbose_name='side')),
                ('side', models.CharField(choices=[
                 ('buy', 'buy'), ('sell', 'sell')], max_length=56, verbose_name='side')),
                ('time_in_force', models.CharField(choices=[('day', 'day'), ('gtc', 'good till cancelled'), ('opg', 'order on open'), (
                    'cls', 'order on close'), ('ioc', 'immediate or cancel'), ('fok', 'fill or kill')], max_length=56, verbose_name='time in force')),
                ('limit_price', models.DecimalField(blank=True, decimal_places=5,
                                                    max_digits=12, null=True, verbose_name='limit price')),
                ('stop_price', models.DecimalField(blank=True, decimal_places=5,
                                                   max_digits=12, null=True, verbose_name='stop price')),
                ('filled_avg_price', models.DecimalField(blank=True, decimal_places=5,
                                                         max_digits=12, null=True, verbose_name='filled average price')),
                ('status', models.CharField(choices=[('new', 'new'), ('partially_filled', 'partially filled'), ('filled', 'filled'), ('done_for_day', 'done for day'), ('canceled', 'canceled'), ('expired', 'expired'), ('replaced', 'replaced'), ('pending_cancel', 'pending cancel'), (
                    'pending_replace', 'pending replace'), ('accepted', 'accepted'), ('pending_new', 'pending new'), ('accepted_for_bidding', 'accepted for bidding'), ('stopped', 'stopped'), ('rejected', 'rejected'), ('suspended', 'suspended'), ('calculated', 'calculated')], max_length=56, verbose_name='status')),
                ('extended_hours', models.BooleanField(default=False)),
                ('trail_price', models.DecimalField(blank=True, decimal_places=5,
                                                    max_digits=12, null=True, verbose_name='trail price')),
                ('trail_percentage', models.DecimalField(blank=True, decimal_places=2,
                                                         max_digits=5, null=True, verbose_name='trail percentage')),
                ('hwm', models.DecimalField(blank=True, decimal_places=5,
                                            max_digits=12, null=True, verbose_name='hwm')),
                ('asset_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                               related_name='+', to='assets.asset', verbose_name='asset id')),
                ('legs', models.ManyToManyField(blank=True, null=True,
                                                related_name='parent', to='orders.Order', verbose_name='legs')),
                ('replaced_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                  related_name='+', to='orders.order', verbose_name='replaced by')),
                ('replaces', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                               related_name='+', to='orders.order', verbose_name='replaces')),
                ('strategy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                               related_name='orders', to='core.strategy', verbose_name='strategy')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                           related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
    ]
