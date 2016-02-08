# coding: utf-8
import logging
import sys
import urllib2

import ijson
import django
from django.apps import apps

from representatives_votes.models import Dossier
from .import_votes import Command

logger = logging.getLogger(__name__)

BASEURL = 'http://parltrack.euwiki.org/'
URL = 'http://parltrack.euwiki.org/dumps/ep_dossiers.json.xz'
LOCAL_PATH = 'ep_dossiers.json.xz'


def parse_dossier_data(data):
    """Parse data from parltarck dossier export (1 dossier) Update dossier
    if it existed before, this function goal is to import and update a
    dossier, not to import all parltrack data
    """
    changed = False
    ref = data['procedure']['reference']

    logger.debug('Processing dossier %s', ref)

    try:
        dossier = Dossier.objects.get(reference=ref)
    except Dossier.DoesNotExist:
        dossier = Dossier(reference=ref)
        logger.debug('Dossier did not exist')
        changed = True

    if dossier.title != data['procedure']['title']:
        logger.debug('Title changed from "%s" to "%s"', dossier.title,
                     data['procedure']['title'])
        dossier.title = data['procedure']['title']
        changed = True

    source = data['meta']['source'].replace('&l=en', '')
    if dossier.link != source:
        logger.debug('Source changed from "%s" to "%s"', dossier.link, source)
        dossier.link = source
        changed = True

    if changed:
        logger.info('Updated dossier %s', ref)
        dossier.save()

    if 'votes' in data.keys() and 'epref' in data['votes']:
        command = Command()
        command.init_cache()
        command.parse_vote_data(data['votes'])


def sync_dossier(reference):
    url = '%s/dossier/%s?format=json' % (BASEURL, reference)

    logger.debug('Syncing dossier from %s' % url)
    with urllib2.urlopen(url) as stream:
        import_single(stream)


def import_single(stream):
    if not apps.ready:
        django.setup()

    for data in ijson.items(stream, ''):
        parse_dossier_data(data)


def main(stream=None):
    if not apps.ready:
        django.setup()

    for data in ijson.items(stream or sys.stdin, 'item'):
        parse_dossier_data(data)
