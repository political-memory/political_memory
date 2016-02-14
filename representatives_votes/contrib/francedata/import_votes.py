# coding: utf-8

import ijson
import logging
import sys

import django
from django.apps import apps
from django.utils.text import slugify

from representatives_votes.models import Proposal, Representative, Vote

logger = logging.getLogger(__name__)


class VotesImporter:
    deputes = None
    scrutins = None
    touched = []

    positions = dict(
        pour="for",
        contre="against",
        abstention="abstain"
    )

    def get_depute(self, prenom, nom):
        if self.deputes is None:
            self.deputes = {
                slugify(r[0]): r[1] for r in
                Representative.objects.values_list('full_name', 'pk')
            }

        full = (u'%s %s' % (prenom, nom)).replace(u' ', ' ')
        return self.deputes.get(slugify(full), None)

    def get_scrutin(self, ref):
        if self.scrutins is None:
            self.scrutins = {
                s[0]: s[1] for s in Proposal.objects.values_list('reference',
                                                                 'pk')
            }

        return self.scrutins.get(ref, None)

    def parse_vote_data(self, data):
        scrutin = self.get_scrutin(data['scrutin_uri'])
        if scrutin is None:
            logger.debug('Cannot import vote for unknown scrutin %s'
                         % data['scrutin_uri'])
            return

        depute = self.get_depute(data['prenom'], data['nom'])
        if depute is None:
            logger.debug('Cannot import vote by unknown rep %s %s'
                         % (data['prenom'], data['nom']))
            return

        if not data['division'].lower() in self.positions:
            logger.debug('Cannot import vote for invalid position %s'
                         % data['division'])
            return
        position = self.positions[data['division'].lower()]

        changed = False
        try:
            vote = Vote.objects.get(representative_id=depute,
                                    proposal_id=scrutin)
        except Vote.DoesNotExist:
            vote = Vote(representative_id=depute, proposal_id=scrutin)
            logger.debug('Created vote for rep %s on %s' % (depute, scrutin))
            changed = True

        if vote.position != position:
            logger.debug('Changed vote position to %s' % position)
            changed = True
            vote.position = position

        if changed:
            logger.debug('Updated vote for rep %s on %s' % (depute, scrutin))
            self.touched.append(scrutin)
            vote.save()

    def update_totals(self):
        proposals = [Proposal.objects.get(pk=pk) for pk in self.touched]

        for proposal in proposals:
            changed = False

            for pos in self.positions.values():
                count = Vote.objects.filter(proposal_id=proposal.pk,
                                            position=pos).count()

                if getattr(proposal, 'total_%s' % pos, None) != count:
                    logger.debug('Changed %s count for proposal %s to %s' % (
                        pos, proposal.pk, count))
                    setattr(proposal, 'total_%s' % pos, count)
                    changed = True

            if changed:
                logger.debug('Updated proposal %s' % proposal.pk)
                proposal.save()


def main(stream=None):
    if not apps.ready:
        django.setup()

    importer = VotesImporter()

    for data in ijson.items(stream or sys.stdin, 'item'):
        importer.parse_vote_data(data)

    importer.update_totals()
