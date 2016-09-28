# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib

from django.db import migrations, models
from django.utils.encoding import smart_str


def calculate_hash(obj):
    """
    Computes fingerprint for an object, this code is duplicated from
    representatives.models.HashableModel because we don't have access to model
    methods in a migration scenario.
    """

    hashable_fields = {
        'Chamber': ['name', 'country', 'abbreviation'],
        'Constituency': ['name'],
        'Group': ['name', 'abbreviation', 'kind', 'chamber'],
        'Mandate': ['group', 'constituency', 'role', 'begin_date', 'end_date',
            'representative']
    }

    fingerprint = hashlib.sha1()
    for field_name in hashable_fields[obj.__class__.__name__]:
        field = obj._meta.get_field(field_name)
        if field.is_relation:
            related = getattr(obj, field_name)
            if related is None:
                fingerprint.update(smart_str(related))
            else:
                fingerprint.update(related.fingerprint)
        else:
            fingerprint.update(smart_str(getattr(obj, field_name)))
    obj.fingerprint = fingerprint.hexdigest()
    return obj.fingerprint


def get_or_create(cls, **kwargs):
    """
    Implements get_or_create logic for models that inherit from
    representatives.models.HashableModel because we don't have access to model
    methods in a migration scenario.
    """

    try:
        obj = cls.objects.get(**kwargs)
        created = False
    except cls.DoesNotExist:
        obj = cls(**kwargs)
        created = True
        calculate_hash(obj)
        obj.save()

    return (obj, created)


def migrate_ep_chamber(apps, schema_editor):
    # Get model managers

    Chamber = apps.get_model("representatives", "Chamber")
    Constituency = apps.get_model("representatives", "Constituency")
    Group = apps.get_model("representatives", "Group")
    Mandate = apps.get_model("representatives", "Mandate")

    # Create EP chamber, constituency and group

    name = 'European Parliament'
    abbr = 'EP'

    ep_chamber, _ = get_or_create(Chamber, name=name, abbreviation=abbr)
    ep_constituency, _ = get_or_create(Constituency, name=name)
    ep_group, _ = get_or_create(Group, name=name, kind='chamber',
        abbreviation=abbr, chamber=ep_chamber)

    # Set chamber on groups

    ep_group_kinds = [
        'committee',
        'delegation',
        'group'
    ]

    Group.objects.filter(kind__in=ep_group_kinds).update(chamber=ep_chamber)

    # Set constituency on EP mandates

    ep_mandate_kinds = [
        'committee',
        'delegation',
        'group',
        'organization'
    ]

    Mandate.objects.filter(group__kind__in=ep_mandate_kinds).update(
        constituency=ep_constituency)

    # Create EP mandates with EP constituency & group with same timespan as
    # the country mandate

    for m in Mandate.objects.filter(group__kind__exact='country'):
        mandate, _ = get_or_create(Mandate,
            representative=m.representative,
            group=ep_group,
            constituency=ep_constituency,
            role=m.role,
            begin_date=m.begin_date,
            end_date=m.end_date
        )


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0015_chamber_abbreviation'),
    ]

    operations = [
        migrations.RunPython(migrate_ep_chamber)
    ]
