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

from celery import shared_task

from legislature.models import MemopolRepresentative
from django.db.models import get_model

@shared_task
def update_representatives_score():
    '''
    Update score for all representatives
    '''
    for representative in MemopolRepresentative.objects.all():
        representative.update_score()

@shared_task
def update_representatives_score_for_proposal(proposal):
    '''
    Update score for representatives that have votes for proposal
    '''
    MemopolVote = get_model('votes', 'MemopolVote')
    for vote in MemopolVote.objects.filter(proposal_id = proposal.id):
        # Extra is the MemopolRepresentative object
        vote.representative.extra.update_score()
