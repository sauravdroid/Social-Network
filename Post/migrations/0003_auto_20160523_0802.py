# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-23 08:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0002_auto_20160518_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='liek',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 23, 8, 2, 47, 218933, tzinfo=utc)),
        ),
    ]
