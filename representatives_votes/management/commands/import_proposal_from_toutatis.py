# coding: utf-8

# This file is part of toutatis.
#
# toutatis is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# toutatis is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Affero Public
# License along with Foobar.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2013 Laurent Peuch <cortex@worlddomination.be>
# Copyright (C) 2015 Arnaud Fabre <af@laquadrature.net>
import json
from urllib2 import urlopen

from django.core.management.base import BaseCommand
from django.conf import settings

from representatives_votes.utils import import_a_dossier

class Command(BaseCommand):
    def handle(self, *args, **options):
        proposal_id = args[0]

        toutatis_server = getattr(settings,
                                  'TOUTATIS_SERVER',
                                  'http://toutatis.mm.staz.be')
        proposal_url = '{}/api/proposals/{}'.format(toutatis_server, proposal_id)
        print('Import proposal from {}'.format(proposal_url))
        proposal_data = json.load(urlopen(proposal_url))
        
        dossier_url = proposal_data['dossier']
        dossier_data = json.load(urlopen(dossier_url))
        # Replace dossier proposals by the one proposal we want
        dossier_data['proposals'] = [proposal_data]

        import_a_dossier(dossier_data)
