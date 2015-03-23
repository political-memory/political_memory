# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0005_auto_20150319_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='active',
        ),
        migrations.RemoveField(
            model_name='mandate',
            name='active',
        ),
    ]
