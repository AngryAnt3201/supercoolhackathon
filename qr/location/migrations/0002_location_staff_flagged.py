# Generated by Django 4.2.6 on 2023-10-21 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='staff_flagged',
            field=models.BooleanField(default=False),
        ),
    ]
