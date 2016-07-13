# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import connection, migrations, models


def create_parl_websites(apps, schema_editor):
    """
    Prepare for remote_id removal by creating WebSite entities from it.
    """

    # Get model managers
    Representative = apps.get_model("representatives", "Representative")
    WebSite = apps.get_model("representatives", "WebSite")

    today = datetime.date.today()

    # EP
    ep_url = 'http://www.europarl.europa.eu/meps/en/%s/_home.html'
    qs = Representative.objects.filter(
        models.Q(mandates__end_date__gte=today) |
        models.Q(mandates__end_date__isnull=True),
        mandates__group__chamber__abbreviation='EP'
    )
    for rep in qs:
        changed = False
        url = ep_url % rep.remote_id

        try:
            site = WebSite.objects.get(representative=rep, kind='EP')
        except WebSite.DoesNotExist:
            site = WebSite(representative=rep, kind='EP', url=url)
            changed = True

        if site.url != url:
            site.url = url
            changed = True

        if changed:
            site.save()

    # AN/SEN
    for chamber in ['AN', 'SEN']:
        qs = Representative.objects.filter(
            models.Q(mandates__end_date__gte=today) |
            models.Q(mandates__end_date__isnull=True),
            mandates__group__chamber__abbreviation=chamber
        )
        for rep in qs:
            changed = False
            url = rep.remote_id

            try:
                site = WebSite.objects.get(representative=rep, kind=chamber)
            except WebSite.DoesNotExist:
                site = WebSite(representative=rep, kind=chamber, url=url)
                changed = True

            if site.url != url:
                site.url = url
                changed = True

            if changed:
                site.save()


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0019_remove_fingerprints'),
    ]

    operations = [
        migrations.RunPython(create_parl_websites),

        migrations.RemoveField(
            model_name='representative',
            name='remote_id',
        ),

        migrations.AlterField(
            model_name='representative',
            name='slug',
            field=models.SlugField(unique=True, max_length=100),
        ),
    ]
