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

    class Meta(ProposalSerializer.Meta):
        fields = ('dossier', 'url',) + ProposalSerializer.Meta.fields


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
        fields = ('dossier',) + ProposalSerializer.Meta.fields + (
            'votes',
        )


class DossierSerializer(serializers.ModelSerializer):
    '''
    Base Dossier Serializer
    '''
    class Meta:
        model = models.Dossier
        fields = (
            'title',
            'reference',
            'text',
            'link',
        )


class DossierHyperLinkedSerializer(DossierSerializer):
    '''
    Dossier Serializer with hyperlinks to proposals
    '''
    proposals = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='proposal-detail',
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
        many=True,
    )

    class Meta(DossierSerializer.Meta):
        fields = DossierSerializer.Meta.fields + (
            'proposals',
        )

    @transaction.atomic
    def create(self, validated_data):
        proposals_data = validated_data.pop('proposals')
        dossier, _ = models.Dossier.objects.get_or_create(**validated_data)
        
        for proposal in models.Proposal.objects.filter(dossier=dossier).all():
            proposal.votes.all().delete()
            proposal.delete()
        
        self._create_proposals(proposals_data, dossier)
        return dossier

    def _create_proposals(self, proposals_data, dossier):
        for proposal_data in proposals_data:
            votes_data = proposal_data.pop('votes')
            proposal_data['dossier'] = dossier
            proposal = models.Proposal.objects.create(**proposal_data)
            for vote_data in votes_data:
                vote_data['proposal'] = proposal
                models.Vote.objects.create(**vote_data)
