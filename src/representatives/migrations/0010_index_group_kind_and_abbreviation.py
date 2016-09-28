# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0009_order_mandates_by_end_date_descendant'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mandate',
            options={'ordering': ('-end_date',)},
        ),
        migrations.AlterField(
            model_name='group',
            name='abbreviation',
            field=models.CharField(default=b'', max_length=10, db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='kind',
            field=models.CharField(max_length=255, db_index=True),
        ),
    ]
