# Generated by Django 3.1.5 on 2021-02-25 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lab', '0016_address_secondary_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Delivery_Charges',
            field=models.FloatField(default=0.0),
        ),
    ]
