# Generated by Django 4.2.3 on 2023-07-07 01:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Domain_auth', '0002_alter_emailverification_expired_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverification',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 7, 4, 21, 54, 730395, tzinfo=datetime.timezone.utc)),
        ),
    ]