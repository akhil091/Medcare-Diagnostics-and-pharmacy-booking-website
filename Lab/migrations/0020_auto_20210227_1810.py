# Generated by Django 3.1.5 on 2021-02-27 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lab', '0019_order_service_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='service_status',
            field=models.CharField(blank=True, choices=[('Incart', 'Incart'), ('Order Placed', 'Order Placed'), ('Arrived', 'Arrived'), ('Collected', 'Collected'), ('Result Out', 'Result Out')], max_length=50, null=True),
        ),
    ]
