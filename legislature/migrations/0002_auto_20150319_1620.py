# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0005_auto_20150319_1620'),
        ('legislature', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='representative',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='representative',
            name='country',
            field=models.ForeignKey(to='representatives.Country', null=True),
            preserve_default=True,
        ),
    ]
