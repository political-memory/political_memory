# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0010_proposal_datetime_index'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dossier',
            unique_together=set([('title', 'reference')]),
        ),
        migrations.AlterUniqueTogether(
            name='proposal',
            unique_together=set([('dossier', 'title', 'reference', 'kind', 'total_abstain', 'total_against', 'total_for')]),
        ),
        migrations.RemoveField(
            model_name='dossier',
            name='fingerprint',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='fingerprint',
        ),
    ]
