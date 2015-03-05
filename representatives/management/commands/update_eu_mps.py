import json
from urllib2 import urlopen

from django.core.management.base import BaseCommand
from django.conf import settings

from representatives.utils import import_representatives_from_format

class Command(BaseCommand):
    def handle(self, *args, **options):
        compotista_server = getattr(settings, 'REPRESENTATIVES_COMPOTISTA_SERVER', 'http://compotista.mm.staz.be')
        import_representatives_from_format(json.load(urlopen(compotista_server + "/latest/")), verbose=True)
