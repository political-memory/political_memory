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
# License along with compotista
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2013 Laurent Peuch <cortex@worlddomination.be>
# Copyright (C) 2015 Arnaud Fabre <af@laquadrature.net>

from django.core.management.base import BaseCommand

from representatives.tasks import sync_from_compotista


class Command(BaseCommand):
    """
    Command to import representative from a compotista server
    """

    def add_arguments(self, parser):
        parser.add_argument('--celery', action='store_true', default=False)

    def handle(self, *args, **options):
        if options['celery']:
            sync_from_compotista.delay()
        else:
            sync_from_compotista()

