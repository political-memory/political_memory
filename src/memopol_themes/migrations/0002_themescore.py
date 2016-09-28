# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memopol_themes', '0001_initial'),
        ('representatives_positions', '0006_positionscore'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThemeScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(default=0)),
            ],
            options={
                'ordering': ['theme__slug'],
                'db_table': 'memopol_themes_themescore',
                'managed': False,
            },
        ),

        migrations.RunSQL(
            """
            CREATE VIEW "memopol_themes_themescore"
            AS SELECT
                "representatives_representative"."id" AS "representative_id",
                "memopol_themes_theme"."id" AS "theme_id",
                SUM(COALESCE("scoresource"."score", 0)) AS "score"
            FROM
                "representatives_representative"
                LEFT OUTER JOIN "memopol_themes_theme"
                    ON 1=1
                LEFT OUTER JOIN (
                    SELECT
                        "representatives_recommendations_dossierscores"."representative_id" AS "representative_id",
                        "memopol_themes_theme"."id" AS "theme_id",
                        "representatives_recommendations_dossierscores"."score" AS "score"
                    FROM
                        "representatives_recommendations_dossierscores"
                        INNER JOIN "memopol_themes_theme_dossiers"
                            ON "memopol_themes_theme_dossiers"."dossier_id" = "representatives_recommendations_dossierscores"."dossier_id"
                        INNER JOIN "memopol_themes_theme"
                            ON "memopol_themes_theme"."id" = "memopol_themes_theme_dossiers"."theme_id"
                    UNION ALL
                    SELECT
                        "representatives_recommendations_votescores"."representative_id" AS "representative_id",
                        "memopol_themes_theme"."id" AS "theme_id",
                        "representatives_recommendations_votescores"."score" AS "score"
                    FROM
                        "representatives_recommendations_votescores"
                        INNER JOIN "memopol_themes_theme_proposals"
                            ON "memopol_themes_theme_proposals"."proposal_id" = "representatives_recommendations_votescores"."proposal_id"
                        INNER JOIN "memopol_themes_theme"
                            ON "memopol_themes_theme"."id" = "memopol_themes_theme_proposals"."theme_id"
                    UNION ALL
                    SELECT
                        "representatives_positions_positionscore"."representative_id" AS "representative_id",
                        "memopol_themes_theme"."id" AS "theme_id",
                        "representatives_positions_positionscore"."score" AS "score"
                    FROM
                        "representatives_positions_positionscore"
                        INNER JOIN "memopol_themes_theme_positions"
                            ON "memopol_themes_theme_positions"."position_id" = "representatives_positions_positionscore"."position_id"
                        INNER JOIN "memopol_themes_theme"
                            ON "memopol_themes_theme"."id" = "memopol_themes_theme_positions"."theme_id"
                ) "scoresource"
                    ON "scoresource"."theme_id" = "memopol_themes_theme"."id"
                    AND "scoresource"."representative_id" = "representatives_representative"."id"
            GROUP BY
                "representatives_representative"."id",
                "memopol_themes_theme"."id"
            """
        ),
    ]
