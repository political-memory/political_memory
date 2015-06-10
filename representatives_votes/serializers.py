# coding: utf-8

# This file is part of toutatis.
#
# toutatis is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# toutatis is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Affero Public
# License along with django-representatives.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2015 Arnaud Fabre <af@laquadrature.net>

import representatives_votes.models as models
from rest_framework import serializers

from django.db import transaction


class VoteSerializer(serializers.ModelSerializer):
    '''
    Serializer for votes
    '''
    class Meta:
        model = models.Vote
        fields = (
            'representative_name',
            'representative_remote_id',
            'position'
        )


class ProposalSerializer(serializers.ModelSerializer):
    '''
    Base Proposal Serializer
    '''
    class Meta:
        model = models.Proposal
        fields = (
            'id',
            'title',
            'description',
            'reference',
            'datetime',
            'kind',
            'total_abstain',
            'total_against',
            'total_for',
        )


class ProposalHyperLinkedSerializer(ProposalSerializer):
    '''
    Proposal Serializer with hyperlink to dossier (used for listing)
    '''
    dossier = serializers.HyperlinkedRelatedField(
        read_only = True,
        view_name = 'dossier-detail',
    )
    
    dossier_title = serializers.CharField(
        read_only = True,
        source = 'dossier.title'
    )

    dossier_reference = serializers.CharField(
        read_only = True,
        source = 'dossier.reference'
    )
    
    class Meta(ProposalSerializer.Meta):
        fields = ProposalSerializer.Meta.fields + (
            'dossier',
            'dossier_title',
            'dossier_reference',
            'url',
        )
        
class ProposalDetailSerializer(ProposalSerializer):
    '''
    Proposal Serializer with votes detail (used in Dossier Detail)
    '''
    votes = VoteSerializer(many=True)
    
    class Meta(ProposalSerializer.Meta):
        fields = ProposalSerializer.Meta.fields + (
            'votes',
        )


class ProposalDetailHyperLinkedSerializer(ProposalDetailSerializer, ProposalHyperLinkedSerializer):
    '''
    Proposal Serializer combined Detail Serializer and Hyperlinked Serializer
    '''
    class Meta(ProposalSerializer.Meta):
        fields = ProposalSerializer.Meta.fields + (
            'dossier',
            'dossier_title',
            'dossier_reference',
            'votes',
        )


class DossierSerializer(serializers.ModelSerializer):
    '''
    Base Dossier Serializer
    '''
    class Meta:
        model = models.Dossier
        fields = (
            'id',
            'title',
            'reference',
            'text',
            'link',
        )


class DossierListSerializer(DossierSerializer):
    '''
    Dossier Serializer with short description of proposals
    '''
    class ProposalSerializer(ProposalSerializer):
        class Meta(ProposalSerializer.Meta):
            fields = (
                'id',
                'url',
            ) + ProposalSerializer.Meta.fields
            
    '''
    proposals = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='proposal-detail',
    )
    '''
    
    proposals = ProposalSerializer(
        many = True,
        read_only = True
    )

    class Meta(DossierSerializer.Meta):
        fields = DossierSerializer.Meta.fields + (
            'url',
            'proposals',
        )


class DossierDetailSerializer(DossierSerializer):
    '''
    Dossier Serializer with proposals details
    '''

    proposals = ProposalDetailSerializer(
        many = True,
    )

    class Meta(DossierSerializer.Meta):
        fields = DossierSerializer.Meta.fields + (
            'proposals',
        )

    @transaction.atomic
    def create(self, validated_data):
        proposals_data = validated_data.pop('proposals')
        dossier, _ = models.Dossier.objects.get_or_create(**validated_data)

        previous_proposals = set(dossier.proposals.all())
        for proposal_data in proposals_data:
            proposal, created = self._create_proposal(
                proposal_data,
                dossier
            )
        if not created:
            previous_proposals.remove(proposal)

        # Delete proposals that don't belongs to that dossier anymore
        for proposal in previous_proposals:
            proposal.delete()

        return dossier

    
    def _create_proposal(self, proposal_data, dossier):
        votes_data = proposal_data.pop('votes')
        proposal_data['dossier'] = dossier
        proposal, created = models.Proposal.objects.get_or_create(**proposal_data)
        if created:
            for vote_data in votes_data:
                vote_data['proposal'] = proposal
                models.Vote.objects.create(**vote_data)
