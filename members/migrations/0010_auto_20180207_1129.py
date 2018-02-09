# Generated by Django 2.0 on 2018-02-07 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_auto_20180206_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instalment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_methode', models.CharField(choices=[('CASH', 'Cash'), ('CRIDIT', 'VISA/MASTER'), ('CHEQUE', 'Cheque')], max_length=11)),
                ('instalment_details', models.CharField(blank=True, max_length=128)),
                ('instalment_date', models.DateField(blank=True)),
                ('instalment_value', models.PositiveIntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_methode', models.CharField(choices=[('CASH', 'Cash'), ('CRIDIT', 'VISA/MASTER'), ('CHEQUE', 'Cheque')], max_length=11)),
                ('payment_details', models.CharField(blank=True, max_length=128)),
                ('payment_date', models.DateField(blank=True)),
                ('payment_total', models.PositiveIntegerField(blank=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.member')),
            ],
        ),
        migrations.AddField(
            model_name='instalment',
            name='payment_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Payment'),
        ),
    ]