# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0007_vote_unique_together_proposal_representative'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='title',
            field=models.CharField(unique=True, max_length=1000),
        ),
    ]
