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


class RepresentativeScoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RepresentativeScore
        fields = ('representative', 'score')


class VoteScoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VoteScore
        fields = ('vote__proposal', 'vote__representative', 'vote__position',
                  'score')
