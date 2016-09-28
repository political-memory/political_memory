# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_positions', '0006_positionscore'),
    ]

    operations = [
        migrations.RunSQL(
            """
            DROP VIEW "representatives_positions_positionscore";
            """
        ),
    ]
