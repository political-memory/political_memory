# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_recommendations', '0006_score_formula'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE FUNCTION decay_score(
                score NUMERIC,
                vote_date timestamp with time zone,
                decay_num NUMERIC,
                decay_denom NUMERIC,
                exponent NUMERIC,
                decimals integer)
            RETURNS NUMERIC AS $$
                SELECT ROUND(
                    CAST(
                        $1 * EXP(
                            GREATEST(
                                -700,
                                LEAST(
                                    700,
                                    -(($3 * EXTRACT(days FROM CURRENT_DATE - $2) / $4) ^ (2 * $5))
                                )
                            )
                        )
                        AS NUMERIC
                    ),
                    $6
                )
            $$ LANGUAGE SQL;
            """
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW "representatives_recommendations_votescores"
            AS SELECT
                representatives_votes_vote.id,
                representatives_votes_vote."position",
                representatives_votes_vote.proposal_id,
                representatives_votes_vote.representative_id,
                decay_score(
                    CAST(CASE
                        WHEN representatives_votes_vote."position"::text = representatives_recommendations_recommendation.recommendation::text THEN representatives_recommendations_recommendation.weight
                        ELSE 0 - representatives_recommendations_recommendation.weight
                    END AS NUMERIC),
                    representatives_votes_proposal.datetime,
                    decay_num.value,
                    decay_denom.value,
                    exponent.value,
                    decimals.value
                ) AS score
            FROM representatives_votes_vote
                JOIN (SELECT CAST(TO_NUMBER(value, '99999') AS NUMERIC) AS value FROM memopol_settings_setting WHERE key = 'SCORE_DECAY_NUM') decay_num ON 1=1
                JOIN (SELECT CAST(TO_NUMBER(value, '99999') AS NUMERIC) AS value FROM memopol_settings_setting WHERE key = 'SCORE_DECAY_DENOM') decay_denom ON 1=1
                JOIN (SELECT CAST(TO_NUMBER(value, '99999') AS NUMERIC) AS value FROM memopol_settings_setting WHERE key = 'SCORE_EXPONENT') exponent ON 1=1
                JOIN (SELECT CAST(TO_NUMBER(value, '99999') AS INTEGER) AS value FROM memopol_settings_setting WHERE key = 'SCORE_DECIMALS') decimals ON 1=1
                JOIN representatives_votes_proposal ON representatives_votes_vote.proposal_id = representatives_votes_proposal.id
                LEFT JOIN representatives_recommendations_recommendation ON representatives_votes_proposal.id = representatives_recommendations_recommendation.proposal_id
            WHERE representatives_recommendations_recommendation.id IS NOT NULL;
            """
        ),
    ]
