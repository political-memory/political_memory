# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0003_auto_20150513_0936'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vote',
            old_name='representative_slug',
            new_name='representative_name',
        ),
    ]
