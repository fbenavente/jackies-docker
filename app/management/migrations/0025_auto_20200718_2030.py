# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2020-07-18 20:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0024_auto_20200718_2023'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cost',
            unique_together=set([('cost_item', 'date')]),
        ),
    ]
