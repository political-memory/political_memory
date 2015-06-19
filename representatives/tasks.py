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

from django.conf import settings

import ijson
from celery import shared_task
from urllib2 import urlopen


from representatives.models import Representative
from representatives.serializers import RepresentativeDetailSerializer


@shared_task
def import_a_representative(data, verbose=False):
    '''
    Import a representative from a serialized
    Python datatypes
    '''
    serializer = RepresentativeDetailSerializer(data=data)
    if serializer.is_valid():
        return serializer.save()
    else:
        # print(data)
        raise Exception(serializer.errors)


@shared_task
def import_representatives_from_compotista(delay=False):
    # Clean data before import
    Representative.objects.all().delete()
    
    compotista_server = getattr(settings,
                                     'COMPOTISTA_SERVER',
                                     'http://compotista.mm.staz.be')
    url = compotista_server + '/export/latest/'
    res = urlopen(url)
    for representative in ijson.items(res, 'item'):
        if delay:
            representative = import_a_representative.delay(representative)
        else:
            representative = import_a_representative(representative)


@shared_task
def export_a_representative(representative):
    '''
    Export a representative to a serialized
    Python datatypes
    '''
    serialized = RepresentativeDetailSerializer(representative)
    return serialized.data


@shared_task
def export_representatives(filters={}):
    return [export_a_representative.delay(representative) for representative in Representative.objects.filter(**filters)]
