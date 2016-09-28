# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0003_auto_20150702_1827'),
        ('representatives_votes', '0002_auto_20150707_1611'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='representative_fingerprint',
        ),
        migrations.AddField(
            model_name='proposal',
            name='representatives',
            field=models.ManyToManyField(
                to='representatives.Representative',
                through='representatives_votes.Vote'),
        ),
    ]
