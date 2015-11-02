# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def remove_duplicate(apps, schema_editor):
    Country = apps.get_model('representatives', 'country')
    Address = apps.get_model('representatives', 'address')
    if Country.objects.filter(pk=12, code='IL').count():
        Address.objects.filter(country_id=12).update(country_id=1121)
        Country.objects.get(pk=12).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0005_auto_20151212_2251'),
    ]

    operations = [
        migrations.RunPython(remove_duplicate)
    ]
