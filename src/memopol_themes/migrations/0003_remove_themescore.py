# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memopol_themes', '0002_themescore'),
    ]

    operations = [
        migrations.RunSQL(
            """
            DROP VIEW "memopol_themes_themescore";
            """
        ),
    ]
