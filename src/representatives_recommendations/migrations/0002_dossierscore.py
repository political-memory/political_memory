# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_recommendations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DossierScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'representatives_recommendations_dossierscores',
                'managed': False,
            },
        ),
        migrations.RunSQL(
            """
            CREATE VIEW "representatives_recommendations_dossierscores"
            AS SELECT
                "representatives_votes_vote"."representative_id" || ':' || "representatives_votes_proposal"."dossier_id" AS "id",
                "representatives_votes_vote"."representative_id",
                "representatives_votes_proposal"."dossier_id",
                SUM(CASE WHEN "representatives_votes_vote"."position" = ("representatives_recommendations_recommendation"."recommendation")
                    THEN "representatives_recommendations_recommendation"."weight"
                    ELSE (0 - "representatives_recommendations_recommendation"."weight")
                END) AS "score"
            FROM "representatives_votes_vote"
            INNER JOIN "representatives_votes_proposal"
                ON ( "representatives_votes_vote"."proposal_id" = "representatives_votes_proposal"."id" )
            LEFT OUTER JOIN "representatives_recommendations_recommendation"
                ON ( "representatives_votes_proposal"."id" = "representatives_recommendations_recommendation"."proposal_id" )
            WHERE "representatives_recommendations_recommendation"."id" IS NOT NULL
            GROUP BY
                "representatives_votes_vote"."representative_id",
                "representatives_votes_proposal"."dossier_id"
            """
        ),
    ]
