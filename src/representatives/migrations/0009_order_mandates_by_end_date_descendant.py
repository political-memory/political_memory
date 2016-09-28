# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0008_constituency_country'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mandate',
            options={'ordering': ('end_date',)},
        ),
    ]
