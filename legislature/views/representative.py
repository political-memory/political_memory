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

from datetime import datetime

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.utils.text import slugify

from core.utils import render_paginate_list
from positions.forms import PositionForm

from ..models import MemopolRepresentative


def index(request, group_kind=None, group=None):

    # Fetch active representatives
    representative_list = MemopolRepresentative.objects.select_related(
        'country',
        'main_mandate',
        'main_mandate__group',
    ).filter(
        active=True
    )

    # Filter the list by group if group information is provided
    if group_kind:
        if group.isnumeric():
            representative_list = representative_list.filter(
                mandates__group_id=int(group),
                mandates__end_date__gte=datetime.now()
            )
        else:
            # Search group based on abbreviation or name
            representative_list = representative_list.filter(
                Q(mandates__group__abbreviation=group) |
                Q(mandates__group__name=group),
                mandates__group__kind=group_kind,
                mandates__end_date__gte=datetime.now()
            )

    # Filter the list by search
    representative_list = _filter_by_search(
        request,
        representative_list
    ).order_by('-score', 'last_name')

    # Grid or list
    if request.GET.get('display') in ('grid', 'list'):
        request.session['display'] = request.GET.get('display')
    if 'display' not in request.session:
        request.session['display'] = 'grid'

    # Render the paginated template
    return render_paginate_list(
        request,
        representative_list,
        'legislature/representative_{}.html'.format(
            request.session['display']
        )
    )


def detail(request, pk=None, name=None):
    try:
        query_set = MemopolRepresentative.objects.select_related(
            'country',
            'main_mandate'
        )
        if pk:
            representative = query_set.get(
                id=pk
            )
        elif name:
            representative = query_set.get(
                slug=name
            )
        else:
            return Http404()
    except MemopolRepresentative.DoesNotExist:
        return Http404()

    position_form = PositionForm()
    return render(
        request,
        'legislature/representative_detail.html',
        {
            'representative': representative,
            'position_form': position_form
        }
    )


def _filter_by_search(request, representative_list):
    """
    Return a representative_list filtered by
    the representative name provided in search form
    """
    search = request.GET.get('search')
    if search:
        return representative_list.filter(
            Q(slug__icontains=slugify(search))
        )
    else:
        return representative_list
