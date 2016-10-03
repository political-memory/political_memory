from rest_framework import serializers

from .models import Recommendation


class RecommendationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Recommendation
        fields = ('recommendation', 'title', 'description', 'weight',
                  'proposal')
        extra_kwargs = {
            'proposal': {'view_name': 'api-proposal-detail'},
        }
