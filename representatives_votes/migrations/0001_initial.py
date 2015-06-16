# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dossier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1000)),
                ('reference', models.CharField(max_length=200)),
                ('text', models.TextField(blank=True)),
                ('link', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1000)),
                ('description', models.TextField(blank=True)),
                ('reference', models.CharField(max_length=200, blank=True)),
                ('datetime', models.DateTimeField()),
                ('kind', models.CharField(max_length=200, blank=True)),
                ('total_abstain', models.IntegerField()),
                ('total_against', models.IntegerField()),
                ('total_for', models.IntegerField()),
                ('dossier', models.ForeignKey(related_name='proposals', to='representatives_votes.Dossier')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('representative_name', models.CharField(max_length=200, blank=True)),
                ('representative_remote_id', models.CharField(max_length=200, blank=True)),
                ('position', models.CharField(max_length=10, choices=[(b'abstain', b'abstain'), (b'for', b'for'), (b'against', b'against')])),
                ('proposal', models.ForeignKey(related_name='votes', to='representatives_votes.Proposal')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
