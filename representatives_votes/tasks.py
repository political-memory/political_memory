# coding: utf-8

# This file is part of toutatis.
#
# toutatis is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# toutatis is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Affero Public
# License along with django-representatives.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2015 Arnaud Fabre <af@laquadrature.net>

from __future__ import absolute_import

import logging
import json

from django.conf import settings

# import redis
from celery import shared_task
from urllib2 import urlopen

from representatives_votes.models import Dossier
from representatives_votes.serializers import DossierDetailSerializer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG)
logger.addHandler(steam_handler)

@shared_task
def import_a_dossier(data):
    '''
    Import a dossier from serialized
    '''
    serializer = DossierDetailSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)

@shared_task
def import_a_dossier_from_toutatis(fingerprint, delay=False):
    '''
    Import a complete dossier from a toutatis server
    '''

    toutatis_server = getattr(settings,
                              'TOUTATIS_SERVER',
                              'http://toutatis.mm.staz.be')
    search_url = '{server}/api/dossiers/?fingerprint={fingerprint}'.format({
        'server': toutatis_server,
        'fingerprint': fingerprint
    })
    logger.info('Import dossier from {}'.format(search_url))
    data = json.load(urlopen(search_url))
    if data['count'] != 1:
        raise Exception('Search should return one and only one result')
    detail_url = data['results'][0]['url']
    data = json.load(urlopen(detail_url))
    if delay:
        import_a_dossier.delay(data)
    else:
        import_a_dossier(data)

@shared_task
def import_a_proposal_from_toutatis(fingerprint, delay=False):
    '''
    Import a partial dossier from a toutatis server
    '''
    pass    

def import_dossiers(data):
    return [import_a_dossier(d_data) for d_data in data]

# Export a dossier
def export_a_dossier(dossier):
    serialized = DossierDetailSerializer(dossier)
    return serialized.data

def export_dossiers(filters={}):
    return [export_a_dossier(dossier) for dossier in Dossier.objects.filter(**filters)]

def export_all_dossier():
    return export_dossiers()
