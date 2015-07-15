# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0004_auto_20150709_1601'),
        ('legislature', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='memopolrepresentative',
            name='main_mandate',
            field=models.ForeignKey(default=True, to='representatives.Mandate', null=True),
        ),
    ]
