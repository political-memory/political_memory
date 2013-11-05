import sys
import json
from django.core.management.base import BaseCommand
from representatives.utils import import_representatives_from_format

class Command(BaseCommand):
    def handle(self, *args, **options):
        import_representatives_from_format(json.load(sys.stdin))
