# Generated by Django 2.0 on 2018-05-16 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paypal_integration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paypalinvoice',
            name='success',
            field=models.NullBooleanField(default=True),
        ),
    ]
