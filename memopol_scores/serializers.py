from rest_framework import serializers

from .models import (
    DossierScore,
    RepresentativeScore,
    VoteScore
)


class DossierScoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DossierScore
        fields = ('representative', 'dossier', 'score')
        extra_kwargs = {
            'representative': {'view_name': 'api-representative-detail'},
            'dossier': {'view_name': 'api-dossier-detail'},
        }


class RepresentativeScoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RepresentativeScore
        fields = ('representative', 'score')
        extra_kwargs = {
            'representative': {'view_name': 'api-representative-detail'},
        }


class VoteScoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VoteScore
        fields = ('vote', 'score')
        extra_kwargs = {
            'vote': {'view_name': 'api-vote-detail'},
        }
