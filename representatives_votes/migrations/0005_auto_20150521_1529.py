# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0004_auto_20150513_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dossier',
            name='title',
            field=models.CharField(max_length=1000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='title',
            field=models.CharField(max_length=1000),
            preserve_default=True,
        ),
    ]
