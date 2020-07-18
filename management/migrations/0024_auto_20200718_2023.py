# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2020-07-18 20:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0023_auto_20180826_1820'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=1, max_digits=6)),
                ('total', models.IntegerField(blank=True, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'cost',
            },
        ),
        migrations.CreateModel(
            name='CostItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('unit', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'cost_item',
            },
        ),
        migrations.AddField(
            model_name='cost',
            name='cost_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.CostItem'),
        ),
    ]
