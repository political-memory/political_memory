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

from django.conf.urls import url

from .views import group, representative

urlpatterns = [
    # List of groups by group kind
    url(
        r'^groups/(?P<kind>\w+)?$',
        group.index,
        name='group-index'
    ),
    # Representative detail by representative name
    url(
        r'^(?P<name>[-\w]+)$',
        representative.detail,
        name='representative-detail'
    ),
    # Representative detail by representative pk
    url(
        r'^(?P<pk>\d+)$',
        representative.detail,
        name='representative-detail'
    ),
    # List of representatives by group kind and group name or pk
    url(
        r'^(?P<group_kind>\w+)/(?P<group>.+)$',
        representative.index,
        name='representative-index'
    ),
    # List all representatives by default
    url(
        r'',
        representative.index,
        name='representative-index'
    ),
]
