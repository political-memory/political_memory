# coding: utf-8

# This file is part of mempol.
#
# mempol is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# mempol is distributed in the hope that it will
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

import django_filters

from .models import MemopolRepresentative


class RepresentativeFilter(django_filters.FilterSet):

    class Meta:
        model = MemopolRepresentative
        # fields = ['full_name', 'country', 'score']
        fields = {
            'full_name': ['icontains', 'exact'],
            'slug': ['exact'],
            'remote_id': ['exact'],
            'gender': ['exact'],
            'active': ['exact'],
            'country__name': ['exact'],
            'country__code': ['exact']
        }

        order_by = ['score', 'full_name']
