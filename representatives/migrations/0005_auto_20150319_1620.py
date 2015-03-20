# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0004_representative_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='representative',
            name='active',
        ),
        migrations.RemoveField(
            model_name='representative',
            name='country',
        ),
    ]
