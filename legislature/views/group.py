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

from datetime import datetime

from django.shortcuts import render

from representatives.models import Group


def index(request, kind=None):
    groups = Group.objects.filter(
        mandates__end_date__gte=datetime.now()
    )
    
    if kind:
        groups = groups.filter(
            kind=kind        
        )
    

    print(groups)

    groups = groups.distinct().order_by('name')
    return render(
        request,
        'legislature/groups_list.html',
        {'groups': groups}
    )
