import pyprind

from django.core.management.base import BaseCommand
from legislature.models import MemopolRepresentative

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        bar = pyprind.ProgBar(MemopolRepresentative.objects.all().count())
        for representative in MemopolRepresentative.objects.all():
            representative.update_score()
            bar.update(item_id = str(representative))
