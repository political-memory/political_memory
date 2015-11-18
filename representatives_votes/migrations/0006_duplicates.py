# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.db.models import Count


def remove_duplicate(apps, schema_editor):
    Vote = apps.get_model('representatives_votes', 'Vote')
    duplicates = Vote.objects.values('proposal_id',
            'representative_id').annotate(Count('id')).filter(id__count__gt=1)

    for duplicate in duplicates:
        remove = Vote.objects.filter(
                proposal_id=duplicate['proposal_id'],
                representative_id=duplicate['representative_id'])

        for i in remove.values_list('pk')[1:]:
            Vote.objects.get(pk=i[0]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0005_make_dossier_reference_unique'),
    ]

    operations = [
        migrations.RunPython(remove_duplicate)
    ]
