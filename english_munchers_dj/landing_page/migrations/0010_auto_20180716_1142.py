# Generated by Django 2.0 on 2018-07-16 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing_page', '0009_auto_20180710_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classrequest',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
