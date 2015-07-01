# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0003_auto_20150616_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memopoldossier',
            name='dossier',
            field=core.fields.AutoOneToOneField(parent_link=True, related_name='extra', primary_key=True, serialize=False, to='representatives_votes.Dossier'),
            preserve_default=True,
        ),
    ]
