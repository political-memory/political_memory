# coding: utf-8

# This file is part of compotista.
#
# compotista is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# compotista is distributed in the hope that it will
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
import ijson
import pyprind

from django.core.management.base import BaseCommand
from django.conf import settings

from urllib2 import urlopen

from representatives.models import Representative
from representatives.utils import import_a_representative

class Command(BaseCommand):
    def handle(self, *args, **options):

        Representative.objects.all().delete()

        self.compotista_server = getattr(settings,
                                    'COMPOTISTA_SERVER',
                                    'http://compotista.mm.staz.be')
        
        url = self.compotista_server + '/export/latest/'
        print('Import representatives from %s' % url)
        
        bar = pyprind.ProgBar(self.get_number_of_meps())
        resource = urlopen(url)
        for i, representative in enumerate(ijson.items(resource, 'item')):
            representative = import_a_representative(representative)
            representative_id = '{} - {}'.format(i, representative.full_name.encode('utf-8'))
            bar.update(item_id = representative_id)

        print(bar)            


    def get_number_of_meps(self):
        response = urlopen(self.compotista_server + '/api/representatives/')
        return int(json.load(response).get('count'))
