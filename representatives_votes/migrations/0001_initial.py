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
                ('title', models.CharField(max_length=500)),
                ('reference', models.CharField(max_length=200)),
                ('text', models.TextField()),
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
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('reference', models.CharField(max_length=200)),
                ('datetime', models.DateTimeField()),
                ('dossier', models.ForeignKey(to='representatives_votes.Dossier')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('representative_slug', models.CharField(max_length=200, null=True, blank=True)),
                ('representative_remote_id', models.CharField(max_length=200, null=True, blank=True)),
                ('position', models.CharField(max_length=10, choices=[(b'abstain', b'abstain'), (b'for', b'for'), (b'against', b'against')])),
                ('proposal', models.ForeignKey(to='representatives_votes.Proposal')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
