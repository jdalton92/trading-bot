# Generated by Django 3.1.6 on 2021-08-17 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_create_bar'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bar',
            unique_together={('asset_id', 't')},
        ),
    ]
