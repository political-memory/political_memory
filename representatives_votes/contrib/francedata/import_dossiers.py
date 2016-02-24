# coding: utf-8

import sys
import ijson
import logging

import django
from django.apps import apps

from representatives_votes.models import Dossier

logger = logging.getLogger(__name__)


def find_dossier(data):
    '''
    Find dossier with reference matching either 'url_an' or 'url_sen',
    create it if not found.  Ensure its reference and source are 'url_an' if
    both fields are present.
    '''

    changed = False
    dossier = None
    reffield = None

    for field in [k for k in ('url_an', 'url_sen') if k in data]:
        try:
            dossier = Dossier.objects.get(reference=data[field])
            reffield = field
            break
        except Dossier.DoesNotExist:
            pass

    if dossier is None:
        reffield = 'url_an' if 'url_an' in data else 'url_sen'
        dossier = Dossier(reference=data[reffield])
        logger.debug('Created dossier %s' % data[reffield])
        changed = True

    if 'url_an' in data and reffield != 'url_an':
        logger.debug('Changed dossier reference to %s' % data['url_an'])
        dossier.reference = data['url_an']
        changed = True

    return dossier, changed


def parse_dossier_data(data):
    dossier, changed = find_dossier(data)

    thisurl = data['url_an' if data['chambre'] == 'AN' else 'url_sen']

    if dossier.reference != dossier.link:
        logger.debug('Changed dossier link to %s' % dossier.reference)
        dossier.link = dossier.reference
        changed = True

    title = data['titre']
    if dossier.reference == thisurl and dossier.title != title:
        logger.debug('Changed dossier title to %s' % title)
        dossier.title = title
        changed = True

    if 'url_an' in data and 'url_sen' in data:
        ext_link = data['url_sen']
        if dossier.ext_link != ext_link:
            logger.debug('Changed dossier ext. link to %s' % ext_link)
            dossier.ext_link = ext_link
            changed = True

    if changed:
        logger.debug('Saved dossier %s' % dossier.reference)
        dossier.save()


def main(stream=None):
    if not apps.ready:
        django.setup()

    for data in ijson.items(stream or sys.stdin, 'item'):
        parse_dossier_data(data)
