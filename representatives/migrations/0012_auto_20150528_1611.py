# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0011_auto_20150528_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='number',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
