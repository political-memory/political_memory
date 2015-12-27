# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0010_index_group_kind_and_abbreviation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ('name',)},
        ),
    ]
