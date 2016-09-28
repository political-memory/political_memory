# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_positions', '0005_set_title'),
        ('representatives_recommendations', '0007_fix_underflow'),
    ]

    operations = [
        migrations.CreateModel(
            name='PositionScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'representatives_positions_positionscore',
                'managed': False,
            },
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW "representatives_positions_positionscore"
            AS SELECT
                "representatives_positions_position"."id" AS "id",
                "representatives_positions_position"."id" AS "position_id",
                "representatives_positions_position"."representative_id" AS "representative_id",
                decay_score(
                    "representatives_positions_position"."score",
                    "representatives_positions_position"."datetime",
                    "decay_num"."value",
                    "decay_denom"."value",
                    "exponent"."value",
                    "decimals"."value"
                ) AS "score"
            FROM "representatives_positions_position"
                JOIN (SELECT CAST(TO_NUMBER(value, '99999') AS NUMERIC) AS value FROM memopol_settings_setting WHERE key = 'SCORE_DECAY_NUM') decay_num ON 1=1
                JOIN (SELECT CAST(TO_NUMBER(value, '99999') AS NUMERIC) AS value FROM memopol_settings_setting WHERE key = 'SCORE_DECAY_DENOM') decay_denom ON 1=1
                JOIN (SELECT CAST(TO_NUMBER(value, '99999') AS NUMERIC) AS value FROM memopol_settings_setting WHERE key = 'SCORE_EXPONENT') exponent ON 1=1
                JOIN (SELECT CAST(TO_NUMBER(value, '99999') AS INTEGER) AS value FROM memopol_settings_setting WHERE key = 'SCORE_DECIMALS') decimals ON 1=1;
            """
        ),
    ]
