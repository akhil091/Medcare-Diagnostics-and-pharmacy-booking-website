# Generated by Django 3.1.5 on 2021-01-27 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('All_Users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Phone', models.CharField(max_length=10)),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('date', models.FloatField(default=1611762016.0889263)),
                ('First_Name', models.CharField(max_length=50)),
                ('Last_Name', models.CharField(max_length=50)),
                ('is_validate', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
    ]
