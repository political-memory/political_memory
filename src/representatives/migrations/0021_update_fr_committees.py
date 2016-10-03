# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def update_kinds(apps, schema_editor):
    """
    Downgrade FR special committees to delegations
    """

    # Get model managers
    Group = apps.get_model("representatives", "Group")

    qs = Group.objects.filter(
        models.Q(name__iregex=ur'^commission d\'enquête') |
        models.Q(name__iregex=ur'^commission spéciale')
    )

    for g in qs:
        g.kind = 'delegation'
        g.save()


def update_abbreviations(apps, schema_editor):
    """
    Migrate to new FR committee abbreviations
    """

    # Get model managers
    Group = apps.get_model("representatives", "Group")

    # Abbreviation mapping
    amap = {
        u'SenComCult': u'Culture',
        u'SenComEco': u'Économie',
        u'SenComDef': u'Défense',
        u'SenComEU': u'Europe',
        u'SenComSoc': u'Social',
        u'SenComFin': u'Finances',
        u'SenComLois': u'Lois',
        u'SenComDevD': u'',
        u'SenComAppL': u'',
        u'AnComCult': u'Culture',
        u'AnComEco': u'Économie',
        u'AnComEtrg': u'Étranger',
        u'AnComDef': u'Défense',
        u'AnComEU': u'Europe',
        u'AnComSoc': u'Social',
        u'AnComFin': u'Finances',
        u'AnComLois': u'Lois',
        u'AnComDevD': u'',
        u'AnComImmu': u'',
    }

    for old, new in amap.iteritems():
        for g in Group.objects.filter(abbreviation=old):
            g.abbreviation = new
            g.save()


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0020_rep_unique_slug_remove_remoteid'),
    ]

    operations = [
        migrations.RunPython(update_kinds),

        migrations.RunPython(update_abbreviations),
    ]
