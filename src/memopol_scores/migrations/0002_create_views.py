# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memopol_scores', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW "memopol_scores_v_vote_score"
            AS SELECT
                "representatives_votes_vote"."id" AS "vote_id",
                decay_score(
                    CAST(CASE
                        WHEN "representatives_votes_vote"."position"::text = "representatives_recommendations_recommendation"."recommendation"::text
                        THEN "representatives_recommendations_recommendation"."weight"
                        ELSE 0 - "representatives_recommendations_recommendation"."weight"
                    END AS NUMERIC),
                    "representatives_votes_proposal"."datetime",
                    "decay_num"."value",
                    "decay_denom"."value",
                    "exponent"."value",
                    "decimals"."value"
                ) AS "score"
            FROM "representatives_votes_vote"
                JOIN (SELECT CAST(TO_NUMBER("value", '99999') AS NUMERIC) AS "value" FROM "memopol_settings_setting" WHERE "key" = 'SCORE_DECAY_NUM') "decay_num" ON 1=1
                JOIN (SELECT CAST(TO_NUMBER("value", '99999') AS NUMERIC) AS "value" FROM "memopol_settings_setting" WHERE "key" = 'SCORE_DECAY_DENOM') "decay_denom" ON 1=1
                JOIN (SELECT CAST(TO_NUMBER("value", '99999') AS NUMERIC) AS "value" FROM "memopol_settings_setting" WHERE "key" = 'SCORE_EXPONENT') "exponent" ON 1=1
                JOIN (SELECT CAST(TO_NUMBER("value", '99999') AS INTEGER) AS "value" FROM "memopol_settings_setting" WHERE "key" = 'SCORE_DECIMALS') "decimals" ON 1=1
                JOIN "representatives_votes_proposal" ON "representatives_votes_vote"."proposal_id" = "representatives_votes_proposal"."id"
                LEFT JOIN "representatives_recommendations_recommendation" ON "representatives_votes_proposal"."id" = "representatives_recommendations_recommendation"."proposal_id"
            WHERE "representatives_recommendations_recommendation"."id" IS NOT NULL;
            """
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW "memopol_scores_v_dossier_score"
            AS SELECT
                "representatives_votes_vote"."representative_id" AS "representative_id",
                "representatives_votes_proposal"."dossier_id" AS "dossier_id",
                SUM("memopol_scores_votescore"."score") AS "score"
            FROM
                "memopol_scores_votescore"
                INNER JOIN "representatives_votes_vote"
                    ON "memopol_scores_votescore"."vote_id" = "representatives_votes_vote"."id"
                INNER JOIN "representatives_votes_proposal"
                    ON "representatives_votes_vote"."proposal_id" = "representatives_votes_proposal"."id"
            GROUP BY
                "representatives_votes_vote"."representative_id",
                "representatives_votes_proposal"."dossier_id"
            """
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW "memopol_scores_v_position_score"
            AS SELECT
                "representatives_positions_position"."id" AS "position_id",
                decay_score(
                    "representatives_positions_position"."score",
                    "representatives_positions_position"."datetime",
                    "decay_num"."value",
                    "decay_denom"."value",
                    "exponent"."value",
                    "decimals"."value"
                ) AS "score"
            FROM
                "representatives_positions_position"
                JOIN (SELECT CAST(TO_NUMBER("value", '99999') AS NUMERIC) AS "value" FROM "memopol_settings_setting" WHERE "key" = 'SCORE_DECAY_NUM') "decay_num" ON 1=1
                JOIN (SELECT CAST(TO_NUMBER("value", '99999') AS NUMERIC) AS "value" FROM "memopol_settings_setting" WHERE "key" = 'SCORE_DECAY_DENOM') "decay_denom" ON 1=1
                JOIN (SELECT CAST(TO_NUMBER("value", '99999') AS NUMERIC) AS "value" FROM "memopol_settings_setting" WHERE "key" = 'SCORE_EXPONENT') "exponent" ON 1=1
                JOIN (SELECT CAST(TO_NUMBER("value", '99999') AS INTEGER) AS "value" FROM "memopol_settings_setting" WHERE "key" = 'SCORE_DECIMALS') "decimals" ON 1=1;
            """
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW "memopol_scores_v_representative_score"
            AS SELECT
                "source"."representative_id" AS "representative_id" ,
                SUM("source"."score") AS "score"
            FROM
                (
                    SELECT
                        "memopol_scores_dossierscore"."representative_id" AS "representative_id",
                        "memopol_scores_dossierscore"."score" AS "score"
                    FROM "memopol_scores_dossierscore"
                    UNION ALL
                    SELECT
                        "representatives_positions_position"."representative_id" AS "representative_id",
                        "memopol_scores_positionscore"."score" AS "score"
                    FROM
                        "memopol_scores_positionscore"
                        INNER JOIN "representatives_positions_position"
                            ON "memopol_scores_positionscore"."position_id" = "representatives_positions_position"."id"
                ) "source"
            GROUP BY
                "source"."representative_id"
            """
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION refresh_vote_scores()
            RETURNS VOID AS $$
            BEGIN
                TRUNCATE TABLE "memopol_scores_votescore";

                INSERT INTO "memopol_scores_votescore" ("vote_id", "score")
                SELECT "vote_id", "score" FROM "memopol_scores_v_vote_score";
            END;
            $$ LANGUAGE PLPGSQL;
            """
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION refresh_dossier_scores()
            RETURNS VOID AS $$
            BEGIN
                TRUNCATE TABLE "memopol_scores_dossierscore";

                PERFORM refresh_vote_scores();

                INSERT INTO "memopol_scores_dossierscore" ("representative_id", "dossier_id", "score")
                SELECT "representative_id", "dossier_id", "score" FROM "memopol_scores_v_dossier_score";
            END;
            $$ LANGUAGE PLPGSQL;
            """
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION refresh_position_scores()
            RETURNS VOID AS $$
            BEGIN
                TRUNCATE TABLE "memopol_scores_positionscore";

                INSERT INTO "memopol_scores_positionscore" ("position_id", "score")
                SELECT "position_id", "score" FROM "memopol_scores_v_position_score";
            END;
            $$ LANGUAGE PLPGSQL;
            """
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION refresh_representative_scores()
            RETURNS VOID AS $$
            BEGIN
                TRUNCATE TABLE "memopol_scores_representativescore";

                PERFORM refresh_dossier_scores();
                PERFORM refresh_position_scores();

                INSERT INTO "memopol_scores_representativescore" ("representative_id", "score")
                SELECT
                    "representatives_representative"."id",
                    COALESCE("memopol_scores_v_representative_score"."score", 0)
                FROM
                    "representatives_representative"
                    LEFT OUTER JOIN "memopol_scores_v_representative_score"
                        ON "memopol_scores_v_representative_score"."representative_id" = "representatives_representative"."id";
            END;
            $$ LANGUAGE PLPGSQL;
            """
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION refresh_scores()
            RETURNS VOID AS $$
            BEGIN
                PERFORM refresh_representative_scores();
            END;
            $$ LANGUAGE PLPGSQL;
            """
        ),
    ]
