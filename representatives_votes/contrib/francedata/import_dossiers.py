# coding: utf-8

import sys
import ijson
import logging
import re

import django
from django.apps import apps
from django.db import transaction

from representatives.contrib.francedata.import_representatives import \
    ensure_chambers
from representatives.models import Chamber
from representatives_votes.models import Document, Dossier

logger = logging.getLogger(__name__)


def extract_reference(url):
    m = re.search(r'/dossier-legislatif/([^./]+)\.html', url)
    if m:
        return m.group(1)

    m = re.search(r'/(\d+)/dossiers/([^./]+)\.asp', url)
    if m:
        return '%s/%s' % (m.group(1), m.group(2))

    m = re.search(r'/dossiers/([^./]+)\.asp', url)
    if m:
        return m.group(1)

    return None


def find_dossier(data):
    '''
    Find dossier with reference matching either 'ref_an' or 'ref_sen',
    create it if not found.  Ensure its reference is 'ref_an' if both fields
    are present.
    '''

    changed = False
    dossier = None
    reffield = None

    for field in [k for k in ('ref_an', 'ref_sen') if k in data]:
        try:
            dossier = Dossier.objects.get(reference=data[field])
            reffield = field
            break
        except Dossier.DoesNotExist:
            pass

    if dossier is None:
        reffield = 'ref_an' if 'ref_an' in data else 'ref_sen'
        dossier = Dossier(reference=data[reffield])
        logger.debug('Created dossier %s' % data[reffield])
        changed = True

    if 'ref_an' in data and reffield != 'ref_an':
        logger.debug('Changed dossier reference to %s' % data['ref_an'])
        dossier.reference = data['ref_an']
        changed = True

    return dossier, changed


def handle_document(dossier, chamber, url):
    doc_changed = False
    try:
        doc = Document.objects.get(chamber=chamber, dossier=dossier,
                                   kind='procedure-file')
    except Document.DoesNotExist:
        doc = Document(chamber=chamber, dossier=dossier, kind='procedure-file')
        logger.debug('Created %s document for dossier %s' %
            (chamber.abbreviation, dossier.title))
        doc_changed = True

    if doc.link != url:
        logger.debug('Changing %s url from %s to %s' %
            (chamber.abbreviation, doc.link, url))
        doc.link = url
        doc_changed = True

    if doc_changed:
        doc.save()


def parse_dossier_data(data, an, sen):
    if 'url_an' in data:
        ref_an = extract_reference(data['url_an'])
        if ref_an is None:
            logger.warn('No reference for dossier %s' % data['url_an'])
            return
        else:
            data['ref_an'] = ref_an

    if 'url_sen' in data:
        ref_sen = extract_reference(data['url_sen'])
        if ref_sen is None:
            logger.warn('No reference for dossier %s' % data['url_sen'])
            return
        else:
            data['ref_sen'] = ref_sen

    dossier, changed = find_dossier(data)

    thisref = data['ref_an' if data['chambre'] == 'AN' else 'ref_sen']

    title = data['titre']
    if dossier.reference == thisref and dossier.title != title:
        logger.debug('Changed dossier title to %s' % title)
        dossier.title = title
        changed = True

    with transaction.atomic():
        if changed:
            logger.debug('Saved dossier %s' % dossier.reference)
            dossier.save()

        if 'url_an' in data:
            handle_document(dossier, an, data['url_an'])

        if 'url_sen' in data:
            handle_document(dossier, sen, data['url_sen'])


def main(stream=None):
    if not apps.ready:
        django.setup()

    ensure_chambers()
    an = Chamber.objects.get(abbreviation='AN')
    sen = Chamber.objects.get(abbreviation='SEN')
    for data in ijson.items(stream or sys.stdin, 'item'):
        parse_dossier_data(data, an, sen)
