# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


def set_site_name(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.filter(pk=settings.SITE_ID).update(
        name=settings.SITE_NAME, domain=settings.SITE_DOMAIN)


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_site_name),
    ]
