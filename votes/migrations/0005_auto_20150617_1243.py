# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0004_auto_20150616_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='memopoldossier',
            name='dossier_reference',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='memopoldossier',
            name='dossier',
            field=models.OneToOneField(parent_link=True, related_name='extra', primary_key=True, serialize=False, to='representatives_votes.Dossier'),
            preserve_default=True,
        ),
    ]
