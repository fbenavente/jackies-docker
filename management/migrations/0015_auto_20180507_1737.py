# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-05-07 17:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0014_auto_20180503_0019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='product',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='productinorder',
            name='discount',
        ),
    ]
