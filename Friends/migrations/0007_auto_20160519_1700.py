# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-19 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Friends', '0006_auto_20160519_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='friend_email',
            field=models.EmailField(max_length=255),
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='friend_email',
            field=models.EmailField(max_length=255),
        ),
        migrations.AlterField(
            model_name='requestlist',
            name='friend_email',
            field=models.EmailField(max_length=255),
        ),
    ]