# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0020_rep_unique_slug_remove_remoteid'),
        ('memopol_themes', '0003_remove_themescore'),
        ('memopol_scores', '0002_create_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThemeScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField()),
                ('representative', models.ForeignKey(related_name='theme_scores', to='representatives.Representative')),
                ('theme', models.ForeignKey(to='memopol_themes.Theme')),
            ],
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW "memopol_scores_v_theme_score"
            AS SELECT
                "scoresource"."representative_id" AS "representative_id",
                "scoresource"."theme_id" AS "theme_id",
                SUM("scoresource"."score") AS "score"
            FROM
                (
                    SELECT
                        "memopol_scores_dossierscore"."representative_id" AS "representative_id",
                        "memopol_themes_theme_dossiers"."theme_id" AS "theme_id",
                        "memopol_scores_dossierscore"."score" AS "score"
                    FROM
                        "memopol_scores_dossierscore"
                        INNER JOIN "memopol_themes_theme_dossiers"
                            ON "memopol_themes_theme_dossiers"."dossier_id" = "memopol_scores_dossierscore"."dossier_id"
                    UNION ALL
                    SELECT
                        "representatives_votes_vote"."representative_id" AS "representative_id",
                        "memopol_themes_theme_proposals"."theme_id" AS "theme_id",
                        "memopol_scores_votescore"."score" AS "score"
                    FROM
                        "memopol_scores_votescore"
                        INNER JOIN "representatives_votes_vote"
                ON "representatives_votes_vote"."id" = "memopol_scores_votescore"."vote_id"
                        INNER JOIN "memopol_themes_theme_proposals"
                            ON "memopol_themes_theme_proposals"."proposal_id" = "representatives_votes_vote"."proposal_id"
                    UNION ALL
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


        migrations.RunSQL(
            """
            DROP FUNCTION refresh_vote_scores();
            """
        ),

        migrations.RunSQL(
            """
            DROP FUNCTION refresh_dossier_scores();
            """
        ),

        migrations.RunSQL(
            """
            DROP FUNCTION refresh_position_scores();
            """
        ),

        migrations.RunSQL(
            """
            DROP FUNCTION refresh_representative_scores();
            """
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION refresh_scores()
            RETURNS VOID AS $$
            BEGIN
                TRUNCATE TABLE "memopol_scores_representativescore";

                TRUNCATE TABLE "memopol_scores_dossierscore";

                TRUNCATE TABLE "memopol_scores_votescore";

                INSERT INTO "memopol_scores_votescore" ("vote_id", "score")
                SELECT "vote_id", "score" FROM "memopol_scores_v_vote_score";

                INSERT INTO "memopol_scores_dossierscore" ("representative_id", "dossier_id", "score")
                SELECT "representative_id", "dossier_id", "score" FROM "memopol_scores_v_dossier_score";

                TRUNCATE TABLE "memopol_scores_positionscore";

                INSERT INTO "memopol_scores_positionscore" ("position_id", "score")
                SELECT "position_id", "score" FROM "memopol_scores_v_position_score";

                TRUNCATE TABLE "memopol_scores_themescore";

                INSERT INTO "memopol_scores_themescore" ("representative_id", "theme_id", "score")
                SELECT
                    "representatives_representative"."id",
                    "memopol_themes_theme"."id",
                    COALESCE("memopol_scores_v_theme_score"."score", 0)
                FROM
                    "representatives_representative"
                    INNER JOIN "memopol_themes_theme" ON 1=1
                    LEFT OUTER JOIN "memopol_scores_v_theme_score"
                        ON "memopol_scores_v_theme_score"."representative_id" = "representatives_representative"."id"
                        AND "memopol_scores_v_theme_score"."theme_id" = "memopol_themes_theme"."id";

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
            SELECT refresh_scores();
            """
        )

    ]
