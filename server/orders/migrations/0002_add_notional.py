# Generated by Django 3.1.6 on 2021-09-20 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='notional',
            field=models.DecimalField(blank=True, decimal_places=5, help_text='Ordered notional amount. If entered, qty will be null.', max_digits=12, null=True, verbose_name='notional'),
        ),
        migrations.AlterField(
            model_name='order',
            name='qty',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=12, null=True, verbose_name='quantity'),
        ),
    ]