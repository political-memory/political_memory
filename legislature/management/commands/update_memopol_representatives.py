from __future__ import absolute_import

from django.db import transaction
from django.core.management.base import BaseCommand

from legislature.models import MemopolRepresentative

class Command(BaseCommand):
    
    @transaction.atomic
    def handle(self, *args, **options):
        for representative in MemopolRepresentative.objects.all():
            representative.update_score()
