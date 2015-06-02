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
        reference = args[0]
        toutatis_server = getattr(settings,
                                  'TOUTATIS_SERVER',
                                  'http://toutatis.mm.staz.be')
        search_url = toutatis_server + '/api/dossiers/?reference=%s' % reference
        print('Import dossier from %s' % search_url)
        data = json.load(urlopen(search_url))
        if data['count'] != 1:
            raise Exception('Search should return one and only one result')
        detail_url = data['results'][0]['url']
        data = json.load(urlopen(detail_url))
        import_a_dossier(data)
