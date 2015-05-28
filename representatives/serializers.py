# coding: utf-8

# This file is part of compotista.
#
# compotista is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# compotista is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Affero Public
# License along with django-representatives.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2015 Arnaud Fabre <af@laquadrature.net>

import representatives.models as models
from rest_framework import serializers

from django.db import transaction

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = ('name', 'code')

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Email
        fields = ('email', 'kind')

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WebSite
        fields = ('url', 'kind')

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Phone
        fields = ('id', 'number', 'kind')

class AddressSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    phones = PhoneSerializer(many=True, source='phone_set')
    class Meta:
        model = models.Address
        fields = ('country', 'city', 'street', 'number', 'postcode', 'floor', 'office_number', 'kind', 'phones')

class ContactField(serializers.Serializer):
    emails = EmailSerializer(many=True)
    phones = PhoneSerializer(many=True)
    websites = WebsiteSerializer(many=True)
    address = AddressSerializer(many=True)
    
    def get_attribute(self, obj):
        return {
            'emails': obj.email_set.all(),
            'websites': obj.website_set.all(),
            'phones': obj.phone_set.all(),
            'address': obj.address_set.all(),
        }


class MandateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='group.name')
    short_id = serializers.CharField(source='group.abbreviation', allow_null=True)
    kind = serializers.CharField(source='group.kind')
    constituency = serializers.CharField(source='constituency.name')
    
    class Meta:
        model = models.Mandate
        fields = (
            'id',
            'name',
            'short_id',
            'kind',
            'constituency',
            'representative',
            'role',
            'representative',
            'begin_date',
            'end_date',
        )


class MandateHyperLinkedSerializer(MandateSerializer):
    class Meta(MandateSerializer.Meta):
        fields = MandateSerializer.Meta.fields + ('url',)


class RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Representative
        fields = (
            'id',
            'slug',
            'remote_id',
            'first_name',
            'last_name',
            'full_name',
            'gender',
            'birth_place',
            'birth_date',
            'photo',
            'active',
        )


class RepresentativeHyperLinkedSerializer(RepresentativeSerializer):
    class Meta(RepresentativeSerializer.Meta):
        fields = RepresentativeSerializer.Meta.fields + ('url',)


class RepresentativeDetailSerializer(RepresentativeSerializer):
    contacts = ContactField()
    mandates = MandateSerializer(many=True, source='mandate_set')
    class Meta(RepresentativeSerializer.Meta):
        fields = RepresentativeSerializer.Meta.fields + (
            'cv',
            'contacts',
            'mandates'
        )
        
    # Nested creation is not implemented yet in DRF, it sucks
    # TODO : fix this code when it will be implemented
    @transaction.atomic
    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        mandates_data = validated_data.pop('mandate_set')
        representative = models.Representative.objects.create(**validated_data)
        
        self._create_mandates(mandates_data, representative)
        self._create_contacts(contacts_data, representative)
        return representative
    
    def _create_contacts(self, contacts_data, representative):
        for contact_data in contacts_data['emails']:
            contact = models.Email(**contact_data)
            contact.representative = representative
            contact.save()

        for contact_data in contacts_data['websites']:
            contact = models.WebSite(**contact_data)
            contact.representative = representative
            contact.save()

        for contact_data in contacts_data['address']:
            country, _ = models.Country.objects.get_or_create(
                **contact_data.pop('country')
            )
            phone_set = contact_data.pop('phone_set')
            contact = models.Address(**contact_data)
            contact.country = country
            contact.representative = representative
            contact.save()

            for phone_data in phone_set:
                phone = models.Phone(**phone_data)
                phone.address = contact
                phone.representative = representative
                phone.save()
            

    def _create_mandates(self, mandates_data, representative):
        for mandate_data in mandates_data:
            constituency, _ = models.Constituency.objects.get_or_create(
                **mandate_data.pop('constituency')
            )
            group, _ = models.Group.objects.get_or_create(
                **mandate_data.pop('group')
            )
            mandate = models.Mandate(**mandate_data)
            mandate.representative = representative
            mandate.constituency = constituency
            mandate.group = group
            mandate.save()
