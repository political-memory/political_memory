# coding: utf-8

from django.db import models

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
                ).select_related(
                    'proposal__dossier',
                    'proposal__recommendation'
                ).order_by('-proposal__datetime', 'proposal__title')
            ),
            'dossierscores'
        )

        return qs

    def get_context_data(self, **kwargs):
        c = super(RepresentativeDetailVotes, self).get_context_data(**kwargs)

        ds = c['object'].dossierscores.all()

        dossiers = {}
        for vote in c['object'].votes.all():
            dossier = vote.proposal.dossier
            pk = dossier.pk
            if pk not in dossiers:
                dossiers[pk] = {
                    'dossier': dossier,
                    'votes': [],
                    'score': [s.score for s in ds if s.dossier_id == pk][0]
                }
            dossiers[pk]['votes'].append(vote)

        c['dossiers'] = dossiers
        c['tab'] = 'votes'

        return c
