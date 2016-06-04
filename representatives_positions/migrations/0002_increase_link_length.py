# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_positions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='link',
            field=models.URLField(max_length=500),
        ),
    ]
