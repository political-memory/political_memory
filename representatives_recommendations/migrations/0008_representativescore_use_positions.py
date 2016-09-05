# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_recommendations', '0007_fix_underflow'),
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
                        "representatives_positions_position"."representative_id" AS "representative_id",
                        "representatives_positions_position"."score" AS "score"
                    FROM  "representatives_positions_position"
                ) "scoresource" ON "scoresource"."representative_id" = "representatives_representative"."id"
            GROUP BY "representatives_representative"."id"
            """
        )
    ]
