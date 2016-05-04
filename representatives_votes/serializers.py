# coding: utf-8

import representatives_votes.models as models

from rest_framework import serializers


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    """
    Vote serializer
    """
    class Meta:
        model = models.Vote
        fields = (
            'proposal',
            'representative',
            'representative_name',
            'position'
        )


class ProposalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Proposal
        fields = (
            'dossier',
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


class ProposalDetailSerializer(ProposalSerializer):
    """ Proposal serializer that includes votes """

    votes = VoteSerializer(many=True)

    class Meta:
        model = models.Proposal
        fields = ProposalSerializer.Meta.fields + ('votes',)


class DossierSerializer(serializers.HyperlinkedModelSerializer):
    """ Base dossier serializer """

    class Meta:
        model = models.Dossier
        fields = (
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

    proposals = ProposalSerializer(many=True)

    class Meta:
        model = models.Dossier
        field = DossierSerializer.Meta.fields + ('proposals',)
