# coding: utf-8

from datetime import datetime
import ijson
import logging
from pytz import timezone as date_timezone
import sys

import django
from django.apps import apps
from django.utils.timezone import make_aware as date_make_aware

from representatives_votes.models import Dossier, Proposal

logger = logging.getLogger(__name__)


def _parse_date(date_str):
    return date_make_aware(
        datetime.strptime(date_str, "%Y-%m-%d"),
        date_timezone('Europe/Paris')
    )


def _get_unique_title(proposal_pk, candidate):
    title = candidate

    try:
        exists = Proposal.objects.get(title=title)
    except Proposal.DoesNotExist:
        exists = None

    if exists and exists.pk != proposal_pk:
        num = 1
        while exists and exists.pk != proposal_pk:
            title = '%s (%d)' % (candidate, num)

            try:
                exists = Proposal.objects.get(title=title)
            except Proposal.DoesNotExist:
                exists = None

            num = num + 1

        logger.debug('Made unique title %s' % title)

    return title


class ScrutinImporter:
    dossiers_ref = None
    dossiers_ext = None

    def get_dossier(self, url):
        if self.dossiers_ref is None:
            self.dossiers_ref = {
                d[0]: d[1] for d in Dossier.objects.values_list('reference',
                                                                'pk')
            }

        if self.dossiers_ext is None:
            self.dossiers_ext = {
                d[0]: d[1] for d in Dossier.objects.exclude(ext_link='')
                .values_list('ext_link', 'pk')
            }

        return self.dossiers_ref.get(url, self.dossiers_ext.get(url, None))

    def parse_scrutin_data(self, data):
        ref = data['url']

        if 'dossier_url' not in data:
            logger.debug('Cannot create proposal without dossier')
            return

        dossier = self.get_dossier(data['dossier_url'])
        if dossier is None:
            logger.debug('Cannot create proposal for unknown dossier %s'
                         % data['dossier_url'])
            return

        changed = False
        try:
            proposal = Proposal.objects.get(reference=ref)
        except Proposal.DoesNotExist:
            proposal = Proposal(reference=ref, total_for=0, total_against=0,
                                total_abstain=0)
            logger.debug('Created proposal %s' % ref)
            changed = True

        values = dict(
            title=_get_unique_title(proposal.pk, data["objet"]),
            datetime=_parse_date(data["date"]),
            dossier_id=dossier,
            kind='dossier'
        )

        for key, value in values.items():
            if value != getattr(proposal, key, None):
                logger.debug('Changed proposal %s to %s' % (key, value))
                setattr(proposal, key, value)
                changed = True

        if changed:
            logger.debug('Updated proposal %s' % ref)
            proposal.save()


def main(stream=None):
    if not apps.ready:
        django.setup()

    importer = ScrutinImporter()

    for data in ijson.items(stream or sys.stdin, 'item'):
        importer.parse_scrutin_data(data)
