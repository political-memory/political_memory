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

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from legislature.models import MemopolRepresentative
from representatives.models import Group


def retrieve(request, pk=None, name=None):
    if pk:
        representative = get_object_or_404(
            MemopolRepresentative,
            id=pk
        )
    elif name:
        representative = get_object_or_404(
            MemopolRepresentative,
            full_name=name
        )
    else:
        return Http404()

    return render(
        request,
        'legislature/representative_view.html',
        {'representative': representative}
    )


def representatives_by_group(request, group_kind, group_abbr=None,
                             group_name=None, search=None, group_id=None):
    if group_id:
        representative_list = MemopolRepresentative.objects.filter(
            mandates__group_id=group_id,
            mandates__end_date__gte=datetime.now()
        )
    elif group_abbr:
        representative_list = MemopolRepresentative.objects.filter(
            mandates__group__abbreviation=group_abbr,
            mandates__group__kind=group_kind,
            mandates__end_date__gte=datetime.now()
        )

    elif group_name:
        representative_list = MemopolRepresentative.objects.filter(
            Q(mandates__group__name__icontains=group_name),
            mandates__group__kind=group_kind,
            mandates__end_date__gte=datetime.now()
        )

    elif search:
        try:
            Group.objects.get(abbreviation=search, kind=group_kind)
            representative_list = MemopolRepresentative.objects.filter(
                mandates__group__abbreviation=search,
                mandates__group__kind=group_kind,
                mandates__end_date__gte=datetime.now()
            )
        except Group.DoesNotExist:
            representative_list = MemopolRepresentative.objects.filter(
                Q(mandates__group__abbreviation__icontains=search) |
                Q(mandates__group__name__icontains=search),
                mandates__group__kind=group_kind,
                mandates__end_date__gte=datetime.now()
            )

    # Select distinct representatives and filter by search
    representative_list = list(set(
        _filter_by_search(request, representative_list)
    ))

    return _render_list(request, representative_list)


def _filter_by_search(request, representative_list):
    """
    Return a representative_list filtered by
    the representative name provided in search form
    """
    search = request.GET.get('search')
    if search:
        return representative_list.filter(
            Q(full_name__icontains=search)
        )
    else:
        return representative_list


def _render_list(request, representative_list, num_by_page=30):
    """
    Render a paginated list of representatives
    """
    paginator = Paginator(representative_list, num_by_page)
    page = request.GET.get('page')
    try:
        representatives = paginator.page(page)
    except PageNotAnInteger:
        representatives = paginator.page(1)
    except EmptyPage:
        representatives = paginator.page(paginator.num_pages)

    context = {}
    queries_without_page = request.GET.copy()
    if 'page' in queries_without_page:
        del queries_without_page['page']
    context['queries'] = queries_without_page

    context['representatives'] = representatives
    context['representative_num'] = paginator.count

    return render(
        request,
        'legislature/representative_list.html',
        context
    )


def groups_by_kind(request, kind):
    groups = Group.objects.filter(
        kind=kind,
        mandates__end_date__gte=datetime.now()
    ).distinct().order_by('name')

    return render(
        request,
        'legislature/groups_list.html',
        {'groups': groups}
    )
