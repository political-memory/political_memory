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

import redis
from celery import shared_task
from urllib2 import urlopen

from representatives_votes.models import Dossier, Proposal, Vote
from representatives.tasks import import_a_model
from representatives_votes.serializers import DossierSerializer, ProposalSerializer, VoteSerializer

logger = logging.getLogger(__name__)

@shared_task
def import_a_dossier_from_toutatis(fingerprint):
    '''
    Import a complete dossier from a toutatis server
    '''
    toutatis_server = settings.TOUTATIS_SERVER
    search_url = '{}/api/dossiers/?fingerprint={}'.format(
        toutatis_server,
        fingerprint
    )
    logger.info('Import dossier with fingerprint {} from {}'.format(
        fingerprint,
        search_url
    ))
    data = json.load(urlopen(search_url))
    if data['count'] != 1:
        raise Exception('Search should return one and only one result')
    detail_url = data['results'][0]['url']
    data = json.load(urlopen(detail_url))
    import_a_model(data, Dossier, DossierSerializer)
    for proposal in data['proposals']:
        logger.info('Import proposal {}'.format(proposal['title']))
        import_a_model(proposal, Proposal, ProposalSerializer)

@shared_task
def import_a_proposal_from_toutatis(fingerprint, delay=False):
    '''
    Import a partial dossier from a toutatis server
    '''
    toutatis_server = settings.TOUTATIS_SERVER
    search_url = '{server}/api/proposals/?fingerprint={fingerprint}'.format({
        'server': toutatis_server,
        'fingerprint': fingerprint
    })
    logger.info('Import proposal with fingerprint {} from {}'.format(
        fingerprint,
        search_url
    ))
    data = json.load(urlopen(search_url))
    if data['count'] != 1:
        raise Exception('Search should return one and only one result')
    detail_url = data['results'][0]['url']
    proposal_data = json.load(urlopen(detail_url))
    dossier_url = proposal_data['dossier']
    dossier_data = json.load(urlopen(dossier_url))
    dossier_data['proposals'] = [proposal_data]
    if delay:
        import_a_dossier.delay(dossier_data)
    else:
        import_a_dossier(dossier_data)

def export_a_dossier(dossier):
    serialized = DossierDetailSerializer(dossier)
    return serialized.data

def export_dossiers(filters={}):
    return [export_a_dossier(dossier) for dossier in Dossier.objects.filter(**filters)]

def export_all_dossier():
    return export_dossiers()
