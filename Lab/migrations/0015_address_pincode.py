# Generated by Django 3.1.5 on 2021-02-25 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lab', '0014_address_zipcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='PinCode',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
