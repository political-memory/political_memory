# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0020_rep_unique_slug_remove_remoteid'),
        ('representatives_votes', '0012_document'),
        ('representatives_positions', '0007_remove_positionscore'),
        ('representatives_recommendations', '0010_remove_views'),
        ('memopol_themes', '0003_remove_themescore'),
        ('memopol_settings', '0002_score_settings'),
    ]

    operations = [
        migrations.CreateModel(
            name='DossierScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField()),
                ('dossier', models.ForeignKey(to='representatives_votes.Dossier')),
                ('representative', models.ForeignKey(related_name='dossier_scores', to='representatives.Representative')),
            ],
        ),
        migrations.CreateModel(
            name='PositionScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField()),
                ('position', models.OneToOneField(related_name='position_score', to='representatives_positions.Position')),
            ],
        ),
        migrations.CreateModel(
            name='RepresentativeScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField()),
                ('representative', models.OneToOneField(related_name='representative_score', to='representatives.Representative')),
            ],
        ),
        migrations.CreateModel(
            name='VoteScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField()),
                ('vote', models.OneToOneField(related_name='vote_score', to='representatives_votes.Vote')),
            ],
        ),
    ]
