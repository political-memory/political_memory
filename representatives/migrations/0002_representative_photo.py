# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='representative',
            name='photo',
            field=models.CharField(max_length=512, null=True),
            preserve_default=True,
        ),
    ]
