# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-05-19 01:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0021_auto_20180517_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='migrated_from_old_system',
            field=models.BooleanField(default=False),
        ),
    ]