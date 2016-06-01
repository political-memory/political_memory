from rest_framework import serializers

from .models import (
    DossierScore,
    Recommendation,
    RepresentativeScore,
    VoteScore
)


class DossierScoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DossierScore
        fields = ('representative', 'dossier', 'score')


class RecommendationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Recommendation
        fields = ('recommendation', 'title', 'description', 'weight',
                  'proposal')


class RepresentativeScoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RepresentativeScore
        fields = ('representative', 'score')


class VoteScoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VoteScore
        fields = ('proposal', 'representative', 'position', 'score')
