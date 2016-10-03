# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_positions', '0002_increase_link_length'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='tags',
        ),
    ]
