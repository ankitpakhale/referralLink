# Generated by Django 4.0.1 on 2022-04-08 03:55

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('CA', '0010_alter_casignup_payment_due_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prsignup',
            name='isMilChukaHai',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='casignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 23, 3, 55, 35, 54362)),
        ),
        migrations.AlterField(
            model_name='offerings',
            name='joiningDate',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='prsignup',
            name='payment_due_date',
            field=models.DateField(default=datetime.datetime(2022, 4, 23, 3, 55, 35, 54030)),
        ),
    ]
