import json
from representatives.models import Representative
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        result = []
        for representative in Representative.objects.all():
            reps = {"id": representative.remote_id}

            result.append(reps)

        print json.dumps(result, indent=4)
