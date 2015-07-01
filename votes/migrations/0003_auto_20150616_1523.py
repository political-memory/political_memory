# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0002_auto_20150616_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memopoldossier',
            name='description',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='memopoldossier',
            name='name',
            field=models.CharField(default=b'', max_length=1000, blank=True),
            preserve_default=True,
        ),
    ]
