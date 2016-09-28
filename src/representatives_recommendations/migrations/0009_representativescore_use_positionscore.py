# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_recommendations', '0008_representativescore_use_positions'),
        ('representatives_positions', '0006_positionscore'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW "representatives_recommendations_representativescore"
            AS
            SELECT
                "representatives_representative"."id" AS "representative_id",
                COALESCE(SUM("scoresource"."score"), 0) AS "score"
            FROM
                "representatives_representative"
                LEFT OUTER JOIN (
                    SELECT
                        "representatives_recommendations_votescores"."representative_id" AS "representative_id",
                        "representatives_recommendations_votescores"."score" AS "score"
                    FROM "representatives_recommendations_votescores"
                    UNION ALL
                    SELECT
                        "representatives_positions_positionscore"."representative_id" AS "representative_id",
                        "representatives_positions_positionscore"."score" AS "score"
                    FROM  "representatives_positions_positionscore"
                ) "scoresource" ON "scoresource"."representative_id" = "representatives_representative"."id"
            GROUP BY "representatives_representative"."id"
            """
        )
    ]
