# coding: utf-8

from django.db import transaction
from rest_framework import serializers

import representatives.models as models


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
        # Don’t validate url, because it could break import of not proper
        # formed url
        return value


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Phone
        fields = ('number', 'kind')

    def validate_phone(self, value):
        return value


class AddressSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = models.Address
        fields = ('country', 'city', 'street',
                  'number', 'postcode', 'floor',
                  'office_number', 'kind',
                  )


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


class ConstituencySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Constituency
        fields = ('id', 'name', 'fingerprint')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Group
        fields = ('id', 'name', 'abbreviation', 'kind', 'fingerprint')


class MandateSerializer(serializers.ModelSerializer):

    # name = serializers.CharField(source='group.name')
    # short_id = serializers.CharField(
    #     source='group.abbreviation', allow_blank=True)
    # kind = serializers.CharField(source='group.kind')
    # constituency = serializers.CharField(source='constituency.name')

    group = serializers.CharField(
        source='group.fingerprint',
    )
    constituency = serializers.CharField(
        source='constituency.fingerprint'
    )
    representative = serializers.CharField(
        source='representative.fingerprint'
    )

    class Meta:
        depth = 1
        model = models.Mandate
        fields = (
            'id',
            'representative',
            'group',
            'constituency',
            'role',
            'begin_date',
            'end_date',
            'fingerprint',
        )

    def to_internal_value(self, data):
        data = super(MandateSerializer, self).to_internal_value(data)
        data['group'] = models.Group.objects.get(
            fingerprint=data['group']['fingerprint']
        )
        data['constituency'] = models.Constituency.objects.get(
            fingerprint=data['constituency']['fingerprint']
        )
        data['representative'] = models.Representative.objects.get(
            fingerprint=data['representative']['fingerprint']
        )
        return data


class MandateDetailSerializer(MandateSerializer):
    group = GroupSerializer()
    constituency = ConstituencySerializer()

    class Meta(MandateSerializer.Meta):
        fields = (
            'id',
            'group',
            'constituency',
            'role',
            'begin_date',
            'end_date',
            'fingerprint',
        )


class RepresentativeSerializer(serializers.ModelSerializer):
    contacts = ContactField()

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
            'cv',
            'contacts',
            'fingerprint',
            'url',
        )

    @transaction.atomic
    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        representative = models.Representative.objects.create(
            **validated_data
        )
        self._create_contacts(contacts_data, representative)
        return representative

    @transaction.atomic
    def update(self, instance, validated_data):
        contacts_data = validated_data.pop('contacts')
        for attr, value in validated_data.iteritems():
            setattr(instance, attr, value)
        instance.save()
        self._create_contacts(contacts_data, instance)
        return instance

    def touch_model(self, model, **data):
        '''
        This method create or look up a model with the given data
        it saves the given model if it exists, updating its
        updated field
        '''
        instance, created = model.objects.get_or_create(**data)

        if not created:
            instance.save()

        return (instance, created)

    def _create_contacts(self, contacts_data, representative):
        for contact_data in contacts_data['emails']:
            contact_data['representative'] = representative
            self.touch_model(model=models.Email, **contact_data)

        for contact_data in contacts_data['websites']:
            contact_data['representative'] = representative
            self.touch_model(model=models.WebSite, **contact_data)

        for contact_data in contacts_data['address']:
            country, _ = models.Country.objects.get_or_create(
                **contact_data.pop('country')
            )
            phone_set = contact_data.pop('phones')
            contact_data['representative'] = representative
            contact_data['country'] = country
            contact, _ = self.touch_model(model=models.Address, **contact_data)

            for phone_data in phone_set:
                phone_data['representative'] = representative
                phone_data['address'] = contact
                self.touch_model(model=models.Phone, **phone_data)


class RepresentativeDetailSerializer(RepresentativeSerializer):

    mandates = MandateDetailSerializer(many=True)

    class Meta(RepresentativeSerializer.Meta):
        fields = RepresentativeSerializer.Meta.fields + (
            'mandates',
        )
