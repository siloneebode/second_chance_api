# Generated by Django 4.2.3 on 2023-09-11 04:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0003_alter_offer_expired_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 13, 4, 42, 53, 763680, tzinfo=datetime.timezone.utc)),
        ),
    ]
