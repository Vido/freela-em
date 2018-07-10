# Generated by Django 2.0 on 2018-07-09 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing_page', '0007_auto_20180423_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='classinfo',
            name='class_length',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='classinfo',
            name='q3_sent',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='classinfo',
            name='q3_sent_msgid',
            field=models.IntegerField(default=0),
        ),
    ]
