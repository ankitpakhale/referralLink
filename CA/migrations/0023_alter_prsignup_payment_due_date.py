# Generated by Django 4.0.3 on 2022-06-15 05:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CA', '0022_alter_prsignup_payment_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prsignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 6, 30, 5, 44, 31, 74320)),
        ),
    ]
