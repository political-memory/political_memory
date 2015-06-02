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

from representatives_votes.models import Dossier
from representatives_votes.serializers import DossierDetailSerializer

# Import a dossier
def import_a_dossier(data):
    serializer = DossierDetailSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
    
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
