# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_recommendations', '0009_representativescore_use_positionscore'),
        ('memopol_themes', '0003_remove_themescore'),
    ]

    operations = [
        migrations.RunSQL(
            """
            DROP VIEW "representatives_recommendations_representativescore";
            """
        ),
        migrations.RunSQL(
            """
            DROP VIEW "representatives_recommendations_dossierscores";
            """
        ),
        migrations.RunSQL(
            """
            DROP VIEW "representatives_recommendations_votescores";
            """
        ),
    ]
