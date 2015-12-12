# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0008_unique_proposal_title'),
        ('votes', '0003_auto_20150709_1601'),
    ]

    operations = [
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
