# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0003_auto_20150702_1827'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='representative',
            options={'ordering': ['last_name', 'first_name']},
        ),
    ]
