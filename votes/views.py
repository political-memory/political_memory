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

from django.shortcuts import get_object_or_404, render

from core.utils import render_paginate_list

from .models import MemopolDossier


def dossier_index(request):
    dossier_list = MemopolDossier.objects.all()

    return render_paginate_list(
        request,
        dossier_list,
        'votes/dossier_index.html'
    )


def dossier_detail(request, pk):
    dossier = get_object_or_404(MemopolDossier, pk=pk)

    return render(
        request,
        'votes/dossier_detail.html',
        {'dossier': dossier}
    )
