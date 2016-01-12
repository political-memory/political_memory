# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0008_unique_proposal_title'),
        ('representatives', '0012_index_group_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recommendation', models.CharField(max_length=10, choices=[(b'abstain', b'abstain'), (b'for', b'for'), (b'against', b'against')])),
                ('title', models.CharField(max_length=1000, blank=True)),
                ('description', models.TextField(blank=True)),
                ('weight', models.IntegerField(default=0)),
                ('proposal', models.OneToOneField(related_name='recommendation', to='representatives_votes.Proposal')),
            ],
            options={
                'ordering': ['proposal__datetime'],
            },
        ),
        migrations.CreateModel(
            name='RepresentativeScore',
            fields=[
                ('representative', models.OneToOneField(related_name='score', primary_key=True, serialize=False, to='representatives.Representative')),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ScoredVote',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('representatives_votes.vote',),
        ),
    ]
