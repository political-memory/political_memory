# coding: utf-8

# This file is part of memopol.
#
# memopol is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# memopol is distributed in the hope that it will
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

from django.conf import settings
from django.utils import timezone

import ijson
import redis
from celery import shared_task
from urllib2 import urlopen

from representatives.models import Representative, Group, Constituency, Mandate, Address, Phone, Email, WebSite
from representatives.serializers import RepresentativeDetailSerializer

logger = logging.getLogger(__name__)

@shared_task
def import_a_representative(data, verbose=False):
    '''
    Import a representative from a serialized
    python datatypes
    '''
    
    # We use a lock to import only one representative at a time
    # Avoid to deal with parallel aspect of importation
    with redis.Redis().lock('import_a_representative'):
        try:
            representative = Representative.objects.get(
                fingerprint=data['fingerprint']
            )
            serializer = RepresentativeDetailSerializer(
                instance=representative,
                data=data
            )
        except:
            serializer = RepresentativeDetailSerializer(data=data)

        if serializer.is_valid():
            return serializer.save()
        else:
            raise Exception(serializer.errors)


@shared_task
def import_representatives_from_compotista(delay=False):
    compotista_server = settings.COMPOTISTA_SERVER
    import_start_datetime = timezone.now()
    url = compotista_server + '/export/latest/'
    res = urlopen(url)

    logger.info(u'Import representative from {}'.format(url))
    for i, representative in enumerate(ijson.items(res, 'item')):
        logger.info(u'{}. Import representative {}'.format(i, representative['full_name']))
        if delay:
            representative = import_a_representative.delay(representative)
        else:
            representative = import_a_representative(representative)

    for model in [Representative, Group, Constituency,
                  Mandate, Address, Phone, Email, WebSite]:
        model.objects.filter(updated__lt=import_start_datetime).delete()


@shared_task
def export_a_representative(representative):
    '''
    Export a representative to a serialized
    Python datatypes
    '''
    serialized = RepresentativeDetailSerializer(representative)
    return serialized.data


@shared_task
def export_representatives(delay=False, **filters):
    if delay:
        return [export_a_representative.delay(representative)
                for representative in Representative.objects.filter(**filters)]
    else:
        return [export_a_representative(representative)
                for representative in Representative.objects.filter(**filters)]
