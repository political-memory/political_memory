from django.core.management.base import BaseCommand

from representatives_recommendations.models import (RepresentativeScore,
    calculate_representative_score)


class Command(BaseCommand):
    def handle(self, *args, **options):
        for score in RepresentativeScore.objects.all():
            score.score = calculate_representative_score(
                score.representative)
            score.save()
