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
import json

from django.conf import settings
from django.utils import timezone

from celery import shared_task
from urllib2 import urlopen

from representatives.models import Representative, Group, Constituency, Mandate, Address, Phone, Email, WebSite
from representatives.serializers import GroupSerializer, ConstituencySerializer, RepresentativeSerializer, MandateSerializer, RepresentativeDetailSerializer

logger = logging.getLogger(__name__)


def import_a_model(data, model, serializer, skip_old=False):
    try:
        instance = model.objects.get(
            fingerprint=data['fingerprint']
        )

        if skip_old:
            # Update 'updated' field
            return instance.save()

        serializer_instance = serializer(
            instance=instance,
            data=data
        )
    except model.DoesNotExist:
        serializer_instance = serializer(
            data=data
        )

    if serializer_instance.is_valid():
        return serializer_instance.save()
    else:
        raise Exception(serializer_instance.errors)


@shared_task
def sync_from_compotista():
    limit = 100
    
    compotista_server = settings.COMPOTISTA_SERVER
    import_start_datetime = timezone.now()

    models_to_import = [{
        'url': compotista_server + '/api/groups',
        'model': Group,
        'serializer': GroupSerializer
    }, {
        'url': compotista_server + '/api/constituencies',
        'model': Constituency,
        'serializer': ConstituencySerializer
    }, {
        'url': compotista_server + '/api/representatives',
        'model': Representative,
        'serializer': RepresentativeSerializer
    }, {
        'url': compotista_server + '/api/mandates',
        'model': Mandate,
        'serializer': MandateSerializer
    }]

    # url = compotista_server + '/'
    # res = urlopen(url)
    for model in models_to_import:
        # Pagination import
        next_url = model['url'] + '?limit={}'.format(limit)
        logger.info(u'Import model {} from {}'.format(model['model'].__name__, model['url']))
        while next_url:
            data = json.load(urlopen(next_url))
            next_url = data['next']
            for model_data in data['results']:
                import_a_model(model_data, model['model'], model['serializer'])            

    logger.info(u'Clean old models')
    # Clean models
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
