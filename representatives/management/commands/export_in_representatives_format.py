import json
from django.core.management.base import BaseCommand
from representatives.utils import export_all_representatives

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        print json.dumps(export_all_representatives(), indent=4)
