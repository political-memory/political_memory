# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0002_auto_20150616_1249'),
        ('votes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memopoldossier',
            name='dossier_ptr',
        ),
        migrations.AddField(
            model_name='memopoldossier',
            name='dossier',
            field=core.fields.AutoOneToOneField(primary_key=True, default=0, serialize=False, to='representatives_votes.Dossier'),
            preserve_default=False,
        ),
    ]
