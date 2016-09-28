# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0014_chamber'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamber',
            name='abbreviation',
            field=models.CharField(default=b'', max_length=10, db_index=True, blank=True),
        ),
    ]
