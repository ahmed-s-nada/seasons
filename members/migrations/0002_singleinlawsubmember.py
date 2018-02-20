# Generated by Django 2.0 on 2018-02-15 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleInLawSubmember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=18)),
                ('last_name', models.CharField(max_length=16)),
                ('gender', models.CharField(choices=[('Mr', 'Male'), ('Mrs', 'Female')], default='Mr', max_length=4)),
                ('birthDay', models.DateField(default='2000-01-01')),
                ('age', models.PositiveIntegerField(editable=False)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profiles')),
                ('sub_member_active', models.BooleanField(default=True)),
                ('job_title', models.CharField(blank=True, max_length=32, null=True)),
                ('company', models.CharField(blank=True, max_length=32, null=True)),
                ('phone', models.CharField(blank=True, max_length=64, null=True)),
                ('email', models.EmailField(max_length=128, null=True)),
                ('main_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='members.member')),
                ('main_sub_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='members.SpouseSubmember')),
            ],
            options={
                'verbose_name': 'Parent',
            },
        ),
    ]