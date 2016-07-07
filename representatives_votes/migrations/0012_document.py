# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.db import migrations, models


def migrate_dossier_links(apps, schema_editor):
    logger = logging.getLogger('migrate_dossier_links')

    # Get model managers
    Chamber = apps.get_model("representatives", "Chamber")
    Dossier = apps.get_model("representatives_votes", "Dossier")
    Document = apps.get_model("representatives_votes", "Document")

    docs = []

    # EP dossiers
    ep_chamber = Chamber.objects.get(abbreviation='EP')
    ep_link = 'europarl.europa.eu'
    for dossier in Dossier.objects.filter(link__icontains=ep_link):
        logger.info('Create document %s for dossier %s' % (dossier.link,
                                                           dossier.reference))
        docs.append(Document(chamber=ep_chamber, dossier=dossier,
                             link=dossier.link, kind='procedure-file'))

    # France dossiers
    try:
        an_chamber = Chamber.objects.get(abbreviation='AN')
        sen_chamber = Chamber.objects.get(abbreviation='SEN')
    except Chamber.DoesNotExist:
        return

    an_link = 'assemblee-nationale.fr'
    sen_link = 'senat.fr'

    for dossier in Dossier.objects.filter(link__icontains=an_link):
        logger.info('Create document %s for dossier %s' % (dossier.link,
                                                           dossier.reference))
        docs.append(Document(chamber=an_chamber, dossier=dossier,
                             link=dossier.link, kind='procedure-file'))

    for dossier in Dossier.objects.filter(ext_link__icontains=an_link):
        logger.info('Create document %s for dossier %s' % (dossier.link,
                                                           dossier.reference))
        docs.append(Document(chamber=an_chamber, dossier=dossier,
                             link=dossier.ext_link, kind='procedure-file'))

    for dossier in Dossier.objects.filter(link__icontains=sen_link):
        logger.info('Create document %s for dossier %s' % (dossier.link,
                                                           dossier.reference))
        docs.append(Document(chamber=sen_chamber, dossier=dossier,
                             link=dossier.link, kind='procedure-file'))

    for dossier in Dossier.objects.filter(ext_link__icontains=an_link):
        logger.info('Create document %s for dossier %s' % (dossier.link,
                                                           dossier.reference))
        docs.append(Document(chamber=sen_chamber, dossier=dossier,
                             link=dossier.ext_link, kind='procedure-file'))

    # Create all dossiers
    logger.info('Saving %s documents...' % len(docs))
    Document.objects.bulk_create(docs)


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0019_remove_fingerprints'),
        ('representatives_votes', '0011_remove_fingerprints'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=1000)),
                ('kind', models.CharField(default=b'', max_length=255, blank=True)),
                ('link', models.URLField(max_length=1000)),
                ('chamber', models.ForeignKey(to='representatives.Chamber')),
                ('dossier', models.ForeignKey(related_name='documents', to='representatives_votes.Dossier')),
            ],
            options={
                'abstract': False,
            },
        ),

        migrations.RunPython(migrate_dossier_links),

        migrations.RemoveField(
            model_name='dossier',
            name='link',
        ),

        migrations.RemoveField(
            model_name='dossier',
            name='ext_link',
        ),
    ]
