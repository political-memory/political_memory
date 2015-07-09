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

import requests

from representatives_votes.tasks import import_a_proposal_from_toutatis
from .forms import RecommendationForm
from .tasks import update_representatives_score as task_urs

    
class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
    

def update_representatives_score(request):
    task_urs.delay()
    return redirect('/admin')
    
def import_vote_with_recommendation(request):
    context = {}
    toutatis_server = getattr(settings,
                              'TOUTATIS_SERVER',
                              'http://toutatis.mm.staz.be')
    
    if request.method == 'POST' and 'search' in request.POST:
        form = SearchForm(request.POST) 
        if form.is_valid():
            query = form.cleaned_data['query']
            context['api_url'] = '{}/api/proposals/?search={}&limit=30'.format(
                toutatis_server,
                query
            )
            r = requests.get(context['api_url'])
            context['results'] = r.json()
    elif request.method == 'POST' and 'create_recommendation' in request.POST:
        form = RecommendationForm(data=request.POST)
        if form.is_valid():
            # First import proposal
            proposal_fingerprint = request.POST['proposal_fingerprint']
            
            proposal = import_a_proposal_from_toutatis(proposal_fingerprint)
            recommendation = form.save(commit=False)
            recommendation.proposal = proposal
            recommendation.save()
        return redirect('/admin/votes/recommendation/')
    else:
        proposal_fingerprint = request.GET.get('import', None)
        if proposal_fingerprint:
            api_url = '{}/api/proposals/?fingerprint={}'.format(
                toutatis_server,
                proposal_fingerprint
            )
            proposal = requests.get(api_url).json()['results'][0]

            context['recommendation_proposal_title'] = proposal['title']
            context['recommendation_proposal_dossier_title'] = proposal['dossier_title']
            context['recommendation_proposal_fingerprint'] = proposal['fingerprint']
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
        proposal_fingerprint = request.GET.get('import', None)
        if proposal_fingerprint:
            import_a_proposal_from_toutatis(proposal_fingerprint)
            return redirect('/admin/')
        form = SearchForm()
    context['form'] = form
    return render(request, 'votes/admin/import.html', context)
