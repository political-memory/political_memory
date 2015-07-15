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

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .digg_paginator import DiggPaginator
from django.shortcuts import render


def render_paginate_list(request, object_list, template_name):
    """
    Render a paginated list of representatives
    """
    pagination_limits = (10, 20, 50, 100)
    num_by_page = request.GET.get('limit', 30)
    paginator = DiggPaginator(object_list, num_by_page, body=5)
    # paginator = Paginator(object_list, num_by_page)
    page = request.GET.get('page', 1)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    context = {}
    queries_without_page = request.GET.copy()
    if 'page' in queries_without_page:
        del queries_without_page['page']
    context['queries'] = queries_without_page
    context['object_list'] = objects
    context['paginator'] = paginator
    context['pagination_limits'] = pagination_limits
    
    return render(
        request,
        template_name,
        context
    )
