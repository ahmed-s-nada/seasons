# Generated by Django 2.0 on 2018-02-07 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0012_auto_20180207_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instalment',
            name='instalment_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(auto_now=True),
        ),
    ]
