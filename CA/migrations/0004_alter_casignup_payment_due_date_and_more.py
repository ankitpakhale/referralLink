# Generated by Django 4.0.1 on 2022-04-09 05:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CA', '0003_alter_casignup_payment_due_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 24, 5, 49, 51, 734080)),
        ),
        migrations.AlterField(
            model_name='offerings',
            name='totalAmount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='prsignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 24, 5, 49, 51, 733746)),
        ),
    ]
