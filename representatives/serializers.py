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

from django.db import transaction

import representatives.models as models
from rest_framework import serializers


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

    def validate_url(self, value):
        '''
        Don’t validate url, because it could break import of not proper formed url
        '''
        return value 

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Phone
        fields = ('number', 'kind')

    def validate_phone(self, value):
        return value

class AddressSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    phones = PhoneSerializer(many=True)
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


class RepresentativeMandateSerializer(MandateSerializer):
    class Meta(MandateSerializer.Meta):
        fields = [elem for elem in MandateSerializer.Meta.fields if elem != 'representative']


class RepresentativeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex', read_only=True)
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
    mandates = RepresentativeMandateSerializer(many=True)
    class Meta(RepresentativeSerializer.Meta):
        fields = RepresentativeSerializer.Meta.fields + (
            'cv',
            'contacts',
            'mandates'
        )


    @transaction.atomic
    def create(self, validated_data):
        """
        Nested creation is not implemented yet in DRF, it sucks We made an
        intensive use of get_or_create to avoid recreating
        representatives The idea here is to truncate all models except
        representatives and recreate them every import.
        TODO : fix this code when it will be implemented
        """

        contacts_data = validated_data.pop('contacts')
        mandates_data = validated_data.pop('mandates')
        representative = models.Representative.objects.update_or_create(
            **validated_data
        )
        self._create_mandates(mandates_data, representative)
        self._create_contacts(contacts_data, representative)
        return representative


    def _create_contacts(self, contacts_data, representative):
        for contact_data in contacts_data['emails']:
            contact_data['representative'] = representative
            models.Email.objects.create(**contact_data)

        for contact_data in contacts_data['websites']:
            contact_data['representative'] = representative
            models.WebSite.objects.create(**contact_data)

        for contact_data in contacts_data['address']:
            country, _ = models.Country.objects.get_or_create(
                **contact_data.pop('country')
            )
            phone_set = contact_data.pop('phones')
            contact_data['representative'] = representative
            contact_data['country'] = country
            contact = models.Address.objects.create(**contact_data)

            for phone_data in phone_set:
                phone_data['representative'] = representative
                phone_data['address'] = contact
                models.Phone.objects.create(**phone_data)

    def _create_mandates(self, mandates_data, representative):
        for mandate_data in mandates_data:
            constituency, _ = models.Constituency.objects.get_or_create(
                **mandate_data.pop('constituency')
            )
            group, _ = models.Group.objects.get_or_create(
                **mandate_data.pop('group')
            )
            mandate_data['representative'] = representative
            mandate_data['constituency'] = constituency
            mandate_data['group'] = group
            models.Mandate.objects.create(**mandate_data)
