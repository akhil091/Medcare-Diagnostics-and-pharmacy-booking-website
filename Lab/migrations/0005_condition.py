# Generated by Django 3.1.5 on 2021-02-14 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lab', '0004_healthpackage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]
