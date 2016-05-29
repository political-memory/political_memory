# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_recommendations', '0004_dossierscore_rewrite'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='representativescore',
            options={
                'managed': False,
                'db_table': 'representatives_recommendations_representativescore',
            },
        ),
        migrations.RunSQL(
            """
            DROP TABLE "representatives_recommendations_representativescore"
            """
        ),
        migrations.RunSQL(
            """
            CREATE VIEW "representatives_recommendations_representativescore"
            AS SELECT
                "representatives_representative"."id" as "representative_id",
                COALESCE(SUM("representatives_recommendations_votescores"."score"), 0) AS "score"
            FROM
                "representatives_representative"
                LEFT OUTER JOIN "representatives_recommendations_votescores"
                    ON "representatives_recommendations_votescores"."representative_id" = "representatives_representative"."id"
            GROUP BY "representatives_representative"."id"
            """
        )
    ]
