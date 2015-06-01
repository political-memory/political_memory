# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0012_auto_20150528_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='url',
            field=models.CharField(max_length=2048, null=True, blank=True),
            preserve_default=True,
        ),
    ]
