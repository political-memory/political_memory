# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0005_auto_20150521_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dossier',
            name='text',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='dossier',
            field=models.ForeignKey(related_name='proposals', to='representatives_votes.Dossier'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vote',
            name='proposal',
            field=models.ForeignKey(related_name='votes', to='representatives_votes.Proposal'),
            preserve_default=True,
        ),
    ]
