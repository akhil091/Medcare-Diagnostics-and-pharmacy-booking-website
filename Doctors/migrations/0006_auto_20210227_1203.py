# Generated by Django 3.1.5 on 2021-02-27 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctors', '0005_auto_20210217_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='allbooking',
            name='Age',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='allbooking',
            name='Email',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='allbooking',
            name='First_Name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='allbooking',
            name='Last_Name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
