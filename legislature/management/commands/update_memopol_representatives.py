from __future__ import absolute_import

from django.db import transaction
from django.core.management.base import BaseCommand

import pyprind

import representatives.models
import legislature.models


class Command(BaseCommand):
    
    @transaction.atomic
    def handle(self, *args, **options):
        bar = pyprind.ProgBar(representatives.models.Representative.objects.all().count())
        for i, representative in enumerate(representatives.models.Representative.objects.all()):
            try:
                memopol_representative = legislature.models.MemopolRepresentative.objects.get(
                    representative_remote_id = representative.remote_id
                )
            except legislature.models.MemopolRepresentative.DoesNotExist:
                memopol_representative = legislature.models.MemopolRepresentative(
                    representative_remote_id = representative.remote_id
                )
            memopol_representative.representative_ptr_id = representative.pk
            
            memopol_representative.__dict__.update(representative.__dict__)
            memopol_representative.save()
            memopol_representative.update_country()
            
            bar.update()
        
        for i, group_item in enumerate(representatives.models.Group.objects.all()):
            memopol_group, _ = legislature.models.MemopolGroup.objects.get_or_create(
                group = group_item
            )
            memopol_group.__dict__.update(group_item.__dict__)
            memopol_group.update_active()
            memopol_group.save()
        
