# Generated by Django 4.0.1 on 2022-04-08 03:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CA', '0011_prsignup_ismilchukahai_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 23, 3, 55, 45, 463214)),
        ),
        migrations.AlterField(
            model_name='prsignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 23, 3, 55, 45, 462880)),
        ),
    ]
