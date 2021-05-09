# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-04-17 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0011_auto_20170331_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='rut',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_source',
            field=models.IntegerField(blank=True, choices=[(1, 'web store'), (2, 'management'), (3, 'pos')], default=1, null=True),
        ),
    ]