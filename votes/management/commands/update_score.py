from django.core.management.base import BaseCommand

from legislature.models import MemopolRepresentative


class Command(BaseCommand):
    def handle(self, *args, **options):
        for rep in MemopolRepresentative.objects.all():
            rep.update_score()
