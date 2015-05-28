# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0009_auto_20150428_0455'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mandate',
            old_name='url',
            new_name='link',
        ),
    ]
