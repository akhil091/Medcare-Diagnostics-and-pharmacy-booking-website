# Generated by Django 3.1.5 on 2021-02-22 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Lab', '0008_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='Package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Lab.healthpackage'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='Test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Lab.tests'),
        ),
    ]
