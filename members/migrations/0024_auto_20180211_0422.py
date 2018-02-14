# Generated by Django 2.0 on 2018-02-11 04:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0023_auto_20180210_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='no_of_submembers',
            field=models.PositiveIntegerField(blank=True, default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='instalment',
            name='instalment_date',
            field=models.DateField(blank=True, default=datetime.date(2018, 2, 11)),
        ),
    ]
