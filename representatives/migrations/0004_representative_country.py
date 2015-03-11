# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0003_auto_20150311_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='representative',
            name='country',
            field=models.ForeignKey(to='representatives.Country', null=True),
            preserve_default=True,
        ),
    ]
