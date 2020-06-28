# -*- coding: utf-8 -*-
from django.contrib.postgres.operations import UnaccentExtension

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0022_order_migrated_from_old_system'),
    ]

    operations = [
        UnaccentExtension()
    ]
