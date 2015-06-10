# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0015_auto_20150603_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='representative',
            name='remote_id',
            field=models.CharField(max_length=255, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
