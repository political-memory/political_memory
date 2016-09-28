# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0008_unique_proposal_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='dossier',
            name='ext_link',
            field=models.URLField(default=b'', blank=True),
        ),
    ]
