# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-05-07 19:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0015_auto_20180507_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comments',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='admin_notes',
            field=models.TextField(null=True),
        ),
    ]
