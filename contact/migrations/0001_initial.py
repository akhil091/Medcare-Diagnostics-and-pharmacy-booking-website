# Generated by Django 3.1.5 on 2021-03-01 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=500)),
                ('Email', models.CharField(max_length=500)),
                ('Contact', models.CharField(max_length=500)),
                ('Subject', models.CharField(max_length=500)),
                ('Message', models.TextField()),
            ],
        ),
    ]