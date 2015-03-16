import json
import urllib2
# from urllib2 import urlopen

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
            json.load(urllib2.urlopen(url)),
            verbose=verbose)
