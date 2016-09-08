# coding: utf-8

from django.db import models

from representatives_votes.models import Vote

from .representative_detail_base import RepresentativeDetailBase


class RepresentativeDetailVotes(RepresentativeDetailBase):
    template_name = 'representatives/representative_detail_votes.html'

    def get_queryset(self):
        qs = super(RepresentativeDetailVotes, self).get_queryset()

        vote_qs = Vote.objects.exclude(proposal__recommendation=None)
        theme = self.get_selected_theme()
        if theme:
            vote_qs = vote_qs.filter(
                models.Q(proposal__dossier__themes__slug=theme)
            )

        qs = qs.prefetch_related(
            models.Prefetch(
                'votes',
                queryset=vote_qs.select_related(
                    'vote_score',
                    'proposal__dossier',
                    'proposal__recommendation'
                ).prefetch_related(
                    'proposal__dossier__themes'
                ).order_by('-proposal__datetime', 'proposal__title')
            ),
            'dossier_scores'
        )

        return qs

    def get_context_data(self, **kwargs):
        c = super(RepresentativeDetailVotes, self).get_context_data(**kwargs)

        ds = c['object'].dossier_scores.all()

        dossiers = {}
        for vote in c['object'].votes.all():
            dossier = vote.proposal.dossier
            pk = dossier.pk
            if pk not in dossiers:
                scores = [s.score for s in ds if s.dossier_id == pk]
                dossiers[pk] = {
                    'dossier': dossier,
                    'votes': [],
                    'score': scores[0] if len(scores) else 0
                }
            dossiers[pk]['votes'].append(vote)

        c['dossiers'] = dossiers
        c['tab'] = 'votes'

        return c
