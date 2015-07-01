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
from django.shortcuts import render, redirect
from django import forms
from django.core.management import call_command

import requests

from representatives_votes.models import Proposal
from .forms import RecommendationForm

    
class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


def import_vote_with_recommendation(request):
    context = {}
    toutatis_server = getattr(settings,
                              'TOUTATIS_SERVER',
                              'http://toutatis.mm.staz.be')
    
    if request.method == 'POST' and 'search' in request.POST:
        form = SearchForm(request.POST) 
        if form.is_valid():
            query = form.cleaned_data['query']
            context['api_url'] = '{}/api/proposals/?search={}&limit=1000'.format(
                toutatis_server,
                query
            )
            r = requests.get(context['api_url'])
            context['results'] = r.json()
    elif request.method == 'POST' and 'create_recommendation' in request.POST:
        form = RecommendationForm(data=request.POST)
        if form.is_valid():
            # First import proposal
            proposal_id = int(request.POST['proposal_id'])
            api_url = '{}/api/proposals/{}'.format(toutatis_server, proposal_id)
            proposal = requests.get(api_url).json()
            
            call_command('import_proposal_from_toutatis', proposal_id, interactive=False)
            # call_command('update_memopol_votes', proposal['dossier_reference'], interactive=False)

            memopol_proposal = Proposal.objects.get(
                title = proposal['title'],
                datetime = proposal['datetime'],
                kind = proposal['kind'],
            )
            recommendation = form.save(commit=False)
            recommendation.proposal = memopol_proposal
            recommendation.save()

            return redirect('/admin/votes/recommendation/')
    else:
        proposal_id = request.GET.get('import', None)
        if proposal_id:
            api_url = '{}/api/proposals/{}'.format(toutatis_server, proposal_id)
            proposal = requests.get(api_url).json()

            context['recommendation_proposal_title'] = proposal['title']
            context['recommendation_proposal_dossier_title'] = proposal['dossier_title']
            context['recommendation_proposal_id'] = proposal_id
            context['recommendation_form'] = RecommendationForm()
        form = SearchForm()
        
    context['form'] = form
    return render(request, 'votes/admin/import.html', context)

def import_vote(request):
    context = {}
    toutatis_server = getattr(settings,
                              'TOUTATIS_SERVER',
                              'http://toutatis.mm.staz.be')
    
    if request.method == 'POST' and 'search' in request.POST:
        print(request.POST)
        form = SearchForm(request.POST) 
        if form.is_valid():
            query = form.cleaned_data['query']
            context['api_url'] = '{}/api/proposals/?search={}&limit=1000'.format(
                toutatis_server,
                query
            )
            r = requests.get(context['api_url'])
            context['results'] = r.json()
    else:
        proposal_id = request.GET.get('import', None)
        if proposal_id:
            # api_url = '{}/api/proposals/{}'.format(toutatis_server, proposal_id)
            # proposal = requests.get(api_url).json()

            call_command('import_proposal_from_toutatis', proposal_id, interactive=False)
            # call_command('update_memopol_votes', proposal['dossier_reference'], interactive=False)
            return redirect('/admin/')
        form = SearchForm()
    context['form'] = form
    return render(request, 'votes/admin/import.html', context)
