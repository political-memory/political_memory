# coding: utf-8

import sys
import ijson
import logging

import django
from django.apps import apps

from representatives_votes.models import Dossier

logger = logging.getLogger(__name__)


def parse_dossier_data(data):
    changed = False
    ref = data['uri']

    try:
        dossier = Dossier.objects.get(reference=ref)
    except Dossier.DoesNotExist:
        dossier = Dossier(reference=ref)
        logger.debug('Created dossier %s' % ref)
        changed = True

    title = data['titre']
    if dossier.title != title:
        logger.debug('Changed dossier title to %s' % title)
        dossier.title = title
        changed = True

    source = data['url']
    if dossier.link != source:
        logger.debug('Changed dossier link to %s' % source)
        dossier.link = source
        changed = True

    if changed:
        logger.debug('Saved dossier %s' % ref)
        dossier.save()


def main(stream=None):
    if not apps.ready:
        django.setup()

    for data in ijson.items(stream or sys.stdin, 'item'):
        parse_dossier_data(data)
