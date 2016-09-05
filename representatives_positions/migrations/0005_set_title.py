# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def set_titles(apps, schema_editor):
    """
    Set position title to first line for multiline positions
    """

    Position = apps.get_model("representatives_positions", "Position")

    for pos in Position.objects.all():
        lines = pos.text.split('\n')
        if len(lines) > 1:
            pos.title = lines[0]
            pos.save()


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_positions', '0004_add_kind_score_title'),
    ]

    operations = [
        migrations.RunPython(set_titles)
    ]
