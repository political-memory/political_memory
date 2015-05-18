# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0002_auto_20150511_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='kind',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='reference',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
    ]
