# This file is part of django-representatives.
#
# django-representatives is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# django-representatives is distributed in the hope that it will
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

# coding: utf-8

import json
from urllib2 import urlopen

from django.core.management.base import BaseCommand
from django.conf import settings

from representatives.utils import import_representatives_from_format


class Command(BaseCommand):

    def handle(self, *args, **options):
        if args and args[0] == 'q':
            verbose = False
        else:
            verbose = True

        compotista_server = getattr(settings,
                                    'REPRESENTATIVES_COMPOTISTA_SERVER',
                                    'http://compotista.mm.staz.be')
        url = compotista_server + "/latest/"
        import_representatives_from_format(
            json.load(urlopen(url)),
            verbose=verbose)
