import json
from urllib2 import urlopen
from django.core.management.base import BaseCommand
from representatives.utils import import_representatives_from_format


class Command(BaseCommand):
    def handle(self, *args, **options):
        import_representatives_from_format(json.load(urlopen("http://compotista.mm.staz.be/latest/")), verbose=True)
