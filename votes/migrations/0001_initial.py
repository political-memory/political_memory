# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemopolDossier',
            fields=[
                ('dossier_ptr', models.OneToOneField(parent_link=True, auto_created=True,
                                                     primary_key=True, serialize=False, to='representatives_votes.Dossier')),
                ('dossier_reference', models.CharField(max_length=200)),
                ('name', models.CharField(default=b'', max_length=1000, blank=True)),
                ('description', models.TextField(default=b'', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('representatives_votes.dossier',),
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False, auto_created=True, primary_key=True)),
                ('recommendation', models.CharField(max_length=10, choices=[
                 (b'abstain', b'abstain'), (b'for', b'for'), (b'against', b'against')])),
                ('title', models.CharField(max_length=1000, blank=True)),
                ('description', models.TextField(blank=True)),
                ('weight', models.IntegerField(default=0)),
                ('proposal', models.OneToOneField(
                    related_name='recommendation', to='representatives_votes.Proposal')),
            ],
        ),
        migrations.CreateModel(
            name='MemopolVote',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('representatives_votes.vote',),
        ),
    ]
