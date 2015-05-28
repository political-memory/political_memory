# coding: utf-8

# This file is part of compotista.
#
# compotista is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# compotista is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Affero Public
# License along with django-representatives.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2013 Laurent Peuch <cortex@worlddomination.be>
# Copyright (C) 2015 Arnaud Fabre <af@laquadrature.net>

from representatives.models import Representative
from representatives.serializers import RepresentativeDetailSerializer

# Import a representative
def import_a_representative(data):
    serializer = RepresentativeDetailSerializer(data=data)
    serializer.is_valid()
    return serializer.save()

def import_representatives(data):
    return [import_a_representative(r_data) for r_data in data]

# Export
def export_a_representative(representative):
    serialized = RepresentativeDetailSerializer(representative)
    return serialized.data

def export_representatives(filters={}):
    return [export_a_representative(representative) for representative in Representative.objects.filter(**filters)]

def export_all_representatives():
    return export_representatives()

def export_active_representatives():
    return export_representatives({'active': True})
