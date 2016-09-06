from django.core.management.base import BaseCommand

from ...models import RepresentativeScore


class Command(BaseCommand):
    help = 'Recomputes all scores'

    def handle(self, *args, **options):
        self.stdout.write('Refreshing scores... ', ending='')
        self.stdout.flush()

        RepresentativeScore.refresh()

        self.stdout.write('done')
