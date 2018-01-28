# Generated by Django 2.0 on 2018-01-27 23:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memebership_code', models.CharField(max_length=6)),
                ('Name', models.CharField(max_length=16)),
                ('membership_start', models.DateField()),
                ('renewal_date', models.DateField()),
                ('days_left_to_renewal', models.IntegerField(editable=False)),
                ('memebership_type', models.CharField(choices=[('F', 'Free'), ('N', 'Annual'), ('L', 'Life Time')], default='N', max_length=1)),
                ('active', models.BooleanField(default=True)),
                ('gender', models.CharField(choices=[('Mr', 'Male'), ('Mrs', 'Female')], default='Mr', max_length=4)),
                ('birthDay', models.DateField(default='1980-01-01')),
                ('Age', models.IntegerField(editable=False)),
                ('job_title', models.CharField(blank=True, max_length=32, null=True)),
                ('company', models.CharField(blank=True, max_length=32, null=True)),
                ('email', models.EmailField(max_length=128)),
                ('email2', models.EmailField(blank=True, max_length=128, null=True)),
                ('phone', models.PositiveIntegerField(blank=True)),
                ('phone2', models.PositiveIntegerField(blank=True, null=True)),
                ('fax', models.PositiveIntegerField(blank=True, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profiles')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('User_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SingleParent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SubMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_membership_type', models.CharField(choices=[('C', 'Child-Under 12'), ('SD', 'Sun/Daughter 12+'), ('S', 'Spouse')], default='S', max_length=1)),
                ('name', models.CharField(max_length=16)),
                ('gender', models.CharField(choices=[('Mr', 'Male'), ('Mrs', 'Female')], default='Mr', max_length=4)),
                ('birthDay', models.DateField(default='2008-01-01')),
                ('job_title', models.CharField(blank=True, max_length=32, null=True)),
                ('company', models.CharField(blank=True, max_length=32, null=True)),
                ('phone', models.PositiveIntegerField(blank=True, null=True)),
                ('email', models.EmailField(max_length=128, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profiles')),
                ('sub_member_active', models.BooleanField(default=True)),
                ('main_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='members.member')),
            ],
        ),
    ]
