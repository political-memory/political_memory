# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0006_duplicates'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('proposal', 'representative')]),
        ),
    ]
