# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memopol_scores', '0003_themescore'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW "memopol_scores_v_theme_score"
            AS SELECT
                "scoresource"."representative_id" AS "representative_id",
                "scoresource"."theme_id" AS "theme_id",
                SUM("scoresource"."score") AS "score"
            FROM
                (
                    -- Score contribution for proposals
                    SELECT
                        "representatives_votes_vote"."representative_id" AS "representative_id",
                        "proposal_themes"."theme_id" AS "theme_id",
                        "memopol_scores_votescore"."score" AS "score"
                    FROM
                        "memopol_scores_votescore"
                        INNER JOIN "representatives_votes_vote"
                            ON "representatives_votes_vote"."id" = "memopol_scores_votescore"."vote_id"
                        INNER JOIN (
                                -- Proposals with a theme
                                SELECT
                                    "representatives_votes_proposal"."id" AS "proposal_id",
                                    "memopol_themes_theme_proposals"."theme_id" AS "theme_id"
                                FROM
                                    "representatives_votes_proposal"
                                    INNER JOIN "memopol_themes_theme_proposals"
                                        ON "representatives_votes_proposal"."id" = "memopol_themes_theme_proposals"."proposal_id"
                                UNION
                                -- Proposals in a dossier with a theme
                                SELECT
                                    "representatives_votes_proposal"."id" AS "proposal_id",
                                    "memopol_themes_theme_dossiers"."theme_id" AS "theme_id"
                                FROM
                                    "representatives_votes_proposal"
                                    INNER JOIN "representatives_votes_dossier"
                                        ON "representatives_votes_dossier"."id" = "representatives_votes_proposal"."dossier_id"
                                    INNER JOIN "memopol_themes_theme_dossiers"
                                        ON "memopol_themes_theme_dossiers"."dossier_id" = "representatives_votes_dossier"."id"
                            ) "proposal_themes"
                            ON "proposal_themes"."proposal_id" = "representatives_votes_vote"."proposal_id"
                    UNION ALL
                    -- Score contribution for positions
                    SELECT
                        "representatives_positions_position"."representative_id" AS "representative_id",
                        "memopol_themes_theme_positions"."theme_id" AS "theme_id",
                        "memopol_scores_positionscore"."score" AS "score"
                    FROM
                        "memopol_scores_positionscore"
                        INNER JOIN "representatives_positions_position"
                            ON "representatives_positions_position"."id" = "memopol_scores_positionscore"."position_id"
                        INNER JOIN "memopol_themes_theme_positions"
                            ON "memopol_themes_theme_positions"."position_id" = "memopol_scores_positionscore"."position_id"
                ) "scoresource"
            GROUP BY
                "scoresource"."representative_id",
                "scoresource"."theme_id"
            """
        ),
    ]
