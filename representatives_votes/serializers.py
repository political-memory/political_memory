# coding: utf-8

import representatives_votes.models as models
from representatives.models import Representative
from rest_framework import serializers


class VoteSerializer(serializers.ModelSerializer):
    """
    Vote serializer
    """
    proposal = serializers.CharField(
        source='proposal.fingerprint'
    )
    representative = serializers.CharField(
        source='representative.fingerprint',
        allow_null=True
    )

    class Meta:
        model = models.Vote
        fields = (
            'id',
            'proposal',
            'representative',
            'representative_name',
            'position'
        )

    def to_internal_value(self, data):
        data = super(VoteSerializer, self).to_internal_value(data)
        data['proposal'] = models.Proposal.objects.get(
            fingerprint=data['proposal']['fingerprint']
        )
        if data['representative']['fingerprint']:
            data['representative'] = Representative.objects.get(
                fingerprint=data['representative']['fingerprint']
            )
        else:
            data['representative'] = None

        return data


class ProposalSerializer(serializers.ModelSerializer):
    dossier = serializers.CharField(
        source='dossier.fingerprint'
    )

    dossier_title = serializers.CharField(
        source='dossier.title',
        read_only=True
    )

    dossier_reference = serializers.CharField(
        source='dossier.reference',
        read_only=True
    )

    class Meta:
        model = models.Proposal
        fields = (
            'id',
            'fingerprint',
            'dossier',
            'dossier_title',
            'dossier_reference',
            'title',
            'description',
            'reference',
            'datetime',
            'kind',
            'total_abstain',
            'total_against',
            'total_for',
            'url',
        )

    def to_internal_value(self, data):
        validated_data = super(ProposalSerializer, self).to_internal_value(
            data)
        validated_data['dossier'] = models.Dossier.objects.get(
            fingerprint=validated_data['dossier']['fingerprint']
        )
        validated_data['votes'] = data['votes']
        return validated_data

    def _create_votes(self, votes_data, proposal):
        for vote in votes_data:
            serializer = VoteSerializer(data=vote)
            if serializer.is_valid():
                serializer.save()
            else:
                raise Exception(serializer.errors)

    def create(self, validated_data):
        votes_data = validated_data.pop('votes')
        proposal = models.Proposal.objects.create(
            **validated_data
        )
        self._create_votes(votes_data, proposal)
        return proposal

    def update(self, instance, validated_data):
        validated_data.pop('votes')
        for attr, value in validated_data.iteritems():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ProposalDetailSerializer(ProposalSerializer):
    """ Proposal serializer that includes votes """
    votes = VoteSerializer(many=True)

    class Meta(ProposalSerializer.Meta):
        fields = ProposalSerializer.Meta.fields + (
            'votes',
        )


class DossierSerializer(serializers.ModelSerializer):
    """ Base dossier serializer """
    class Meta:
        model = models.Dossier
        fields = (
            'id',
            'fingerprint',
            'title',
            'reference',
            'text',
            'link',
            'url',
        )


class DossierDetailSerializer(DossierSerializer):
    """
    Dossier serializer that includes proposals and votes.
    """
    proposals = ProposalDetailSerializer(many=True)

    class Meta(DossierSerializer.Meta):
        fields = DossierSerializer.Meta.fields + (
            'proposals',
        )
