# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_recommendations', '0005_representativescore'),
        ('representatives_positions', '0004_add_kind_score_title'),
        ('memopol_settings', '0002_score_settings'),
    ]

    operations = [
        migrations.RunSQL(
            """
            DROP VIEW "representatives_recommendations_votescores" CASCADE;
            """
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='weight',
            field=models.FloatField(default=0),
        ),
        migrations.RunSQL(
            """
            CREATE VIEW "representatives_recommendations_votescores"
            AS SELECT
                representatives_votes_vote.id,
                representatives_votes_vote."position",
                representatives_votes_vote.proposal_id,
                representatives_votes_vote.representative_id,
                ROUND(CAST(EXP(-((decay_num.value * EXTRACT(days FROM CURRENT_DATE - representatives_votes_proposal.datetime) / decay_denom.value) ^ (2 * exponent.value)))
                    * (CASE
                        WHEN representatives_votes_vote."position"::text = representatives_recommendations_recommendation.recommendation::text THEN representatives_recommendations_recommendation.weight
                        ELSE 0 - representatives_recommendations_recommendation.weight
                    END) AS NUMERIC), decimals.value) AS score
            FROM representatives_votes_vote
                JOIN (SELECT CAST(TO_NUMBER(value, '99999') AS FLOAT) AS value FROM memopol_settings_setting WHERE key = 'SCORE_DECAY_NUM') decay_num ON 1=1
                JOIN (SELECT CAST(TO_NUMBER(value, '99999') AS FLOAT) AS value FROM memopol_settings_setting WHERE key = 'SCORE_DECAY_DENOM') decay_denom ON 1=1
                JOIN (SELECT CAST(TO_NUMBER(value, '99999') AS FLOAT) AS value FROM memopol_settings_setting WHERE key = 'SCORE_EXPONENT') exponent ON 1=1
                JOIN (SELECT CAST(TO_NUMBER(value, '99999') AS INTEGER) AS value FROM memopol_settings_setting WHERE key = 'SCORE_DECIMALS') decimals ON 1=1
                JOIN representatives_votes_proposal ON representatives_votes_vote.proposal_id = representatives_votes_proposal.id
                LEFT JOIN representatives_recommendations_recommendation ON representatives_votes_proposal.id = representatives_recommendations_recommendation.proposal_id
            WHERE representatives_recommendations_recommendation.id IS NOT NULL;
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
