# Generated by Django 2.0 on 2018-02-07 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0016_auto_20180207_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='last_payment_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
