# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_recommendations', '0003_votescore'),
    ]

    operations = [
    	migrations.RunSQL(
    		"""
    		DROP VIEW "representatives_recommendations_dossierscores"
    		"""
    	),
        migrations.RunSQL(
            """
            CREATE VIEW "representatives_recommendations_dossierscores"
            AS SELECT
                "representatives_recommendations_votescores"."representative_id" || ':' || "representatives_votes_proposal"."dossier_id" AS "id",
                "representatives_recommendations_votescores"."representative_id",
                "representatives_votes_proposal"."dossier_id",
                SUM("representatives_recommendations_votescores"."score") AS "score"
            FROM "representatives_recommendations_votescores"
            INNER JOIN "representatives_votes_proposal"
                ON ( "representatives_recommendations_votescores"."proposal_id" = "representatives_votes_proposal"."id" )
            GROUP BY
                "representatives_recommendations_votescores"."representative_id",
                "representatives_votes_proposal"."dossier_id"
            """
        ),
    ]
