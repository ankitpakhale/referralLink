# Generated by Django 4.0.1 on 2022-04-06 12:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CA', '0007_alter_casignup_payment_due_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 21, 12, 26, 23, 732115)),
        ),
        migrations.AlterField(
            model_name='prsignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 21, 12, 26, 23, 731793)),
        ),
    ]
