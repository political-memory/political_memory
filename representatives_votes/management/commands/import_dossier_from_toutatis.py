import json
import urllib2

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        dossier_ref = args[0]
        print(dossier_ref)
