# Generated by Django 2.0 on 2018-05-17 13:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('paypal_integration', '0003_auto_20180516_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='paypalinvoice',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2018, 5, 17, 13, 3, 55, 982296, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
