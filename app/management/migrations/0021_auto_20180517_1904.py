# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-05-17 19:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0020_auto_20180517_1902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flavor',
            name='order',
        ),
        migrations.RemoveField(
            model_name='size',
            name='order',
        ),
    ]