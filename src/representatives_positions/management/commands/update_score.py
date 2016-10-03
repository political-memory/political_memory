from django.core.management.base import BaseCommand

from positions.models import (RepresentativeVoteProfile,
                              calculate_representative_score)


class Command(BaseCommand):
    def handle(self, *args, **options):
        for profile in RepresentativeVoteProfile.objects.all():
            profile.score = calculate_representative_score(
                profile.representative)
            profile.save()
