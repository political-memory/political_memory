# coding: utf-8

from django.db import models
from django.views import generic

from representatives.models import Representative
from representatives_recommendations.models import VoteScore
from representatives_votes.models import Proposal

from .representative_detail_base import RepresentativeDetailBase


class RepresentativeDetailVotes(RepresentativeDetailBase):
    template_name = 'representatives/representative_detail_votes.html'

    def get_queryset(self):
        qs = super(RepresentativeDetailVotes, self).get_queryset()

        qs = qs.prefetch_related(
            models.Prefetch(
                'votes',
                queryset=VoteScore.objects.filter(
                    proposal__in=Proposal.objects.exclude(recommendation=None),
                ).select_related('proposal__recommendation').order_by(
                    '-proposal__datetime')
            )
        )

        return qs

    def get_context_data(self, **kwargs):
        c = super(RepresentativeDetailVotes, self).get_context_data(**kwargs)

        c['tab'] = 'votes'
        c['votes'] = c['object'].votes.all()

        return c
