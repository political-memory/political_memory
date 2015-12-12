# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legislature', '0002_memopolrepresentative_main_mandate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memopolrepresentative',
            name='main_mandate',
            field=models.ForeignKey(
                default=None, to='representatives.Mandate', null=True),
        ),
    ]
