# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0010_auto_20150527_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='address',
            field=models.ForeignKey(to='representatives.Address', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='phone',
            name='number',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
    ]
