# Generated by Django 3.1.5 on 2021-02-23 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('All_Users', '0024_auto_20210223_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date',
            field=models.FloatField(default=1614107318.7700527),
        ),
    ]