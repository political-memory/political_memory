# coding: utf-8

from django.db import models
from django.views import generic

from representatives.models import Representative
from representatives_recommendations.models import VoteScore
from representatives_votes.models import Proposal

from .representative_mixin import RepresentativeViewMixin


class RepresentativeVotes(RepresentativeViewMixin, generic.DetailView):
    template_name = 'representatives/representative_votes'

    queryset = Representative.objects.select_related('score')

    def get_queryset(self):
        qs = super(RepresentativeVotes, self).get_queryset()

        qs = self.prefetch_for_representative_country_and_main_mandate(qs)

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
        c = super(RepresentativeVotes, self).get_context_data(**kwargs)

        self.add_representative_country_and_main_mandate(c['object'])

        c['votes'] = c['object'].votes.all()

        return c
