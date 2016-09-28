# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_constituencies(apps, schema_editor):
    """
    Re-save constituencies to recompute fingerprints
    """
    Constituency = apps.get_model("representatives", "Constituency")
    for c in Constituency.objects.all():
        c.save()


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0016_chamber_migrate_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mandate',
            name='role',
            field=models.CharField(default=b'', help_text=b'Eg.: president of a political group', max_length=255, blank=True),
        ),

        migrations.RunPython(migrate_constituencies)
    ]
