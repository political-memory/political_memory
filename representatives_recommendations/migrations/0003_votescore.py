# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_recommendations', '0002_dossierscore'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.CharField(max_length=10)),
                ('score', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['proposal__datetime'],
                'db_table': 'representatives_recommendations_votescores',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='ScoredVote',
        ),
        migrations.RunSQL(
            """
            CREATE VIEW "representatives_recommendations_votescores"
            AS SELECT
                "representatives_votes_vote"."id",
                "representatives_votes_vote"."position",
                "representatives_votes_vote"."proposal_id",
                "representatives_votes_vote"."representative_id",
                CASE WHEN "representatives_votes_vote"."position" = ("representatives_recommendations_recommendation"."recommendation")
                    THEN "representatives_recommendations_recommendation"."weight"
                    ELSE (0 - "representatives_recommendations_recommendation"."weight")
                END AS "score"
            FROM "representatives_votes_vote"
            INNER JOIN "representatives_votes_proposal"
                ON ( "representatives_votes_vote"."proposal_id" = "representatives_votes_proposal"."id" )
            LEFT OUTER JOIN "representatives_recommendations_recommendation"
                ON ( "representatives_votes_proposal"."id" = "representatives_recommendations_recommendation"."proposal_id" )
            WHERE "representatives_recommendations_recommendation"."id" IS NOT NULL
            """
        )
    ]
