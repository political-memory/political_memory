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
            'position'
        )
        extra_kwargs = {
            'proposal': {'view_name': 'api-proposal-detail'},
            'representative': {'view_name': 'api-representative-detail'}
        }


class ProposalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Proposal
        fields = (
            'id',
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

        extra_kwargs = {
            'dossier': {'view_name': 'api-dossier-detail'},
            'url': {'view_name': 'api-proposal-detail'}
        }


class ProposalDetailSerializer(ProposalSerializer):
    """ Proposal serializer that includes votes """

    votes = VoteSerializer(many=True)

    class Meta(ProposalSerializer.Meta):
        fields = ProposalSerializer.Meta.fields + ('votes',)


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    """ Base document serializer """

    class Meta:
        model = models.Document
        fields = (
            'id',
            'dossier',
            'chamber',
            'kind',
            'link'
        )

        extra_kwargs = {
            'dossier': {'view_name': 'api-dossier-detail'},
            'chamber': {'view_name': 'api-chamber-detail'}
        }


class DossierSerializer(serializers.HyperlinkedModelSerializer):
    """ Base dossier serializer """

    class Meta:
        model = models.Dossier
        fields = (
            'id',
            'url',
            'title',
            'reference',
            'text',
        )
        extra_kwargs = {
            'url': {'view_name': 'api-dossier-detail'}
        }


class DossierDetailSerializer(DossierSerializer):
    """
    Dossier serializer that includes proposals and votes.
    """

    proposals = ProposalSerializer(many=True)
    documents = DocumentSerializer(many=True)

    class Meta(DossierSerializer.Meta):
        fields = DossierSerializer.Meta.fields + ('proposals', 'documents')
