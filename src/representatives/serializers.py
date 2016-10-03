# coding: utf-8

from rest_framework import serializers

import representatives.models as models


class CountrySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Country
        fields = ('id', 'url', 'name', 'code')
        extra_kwargs = {
            'url': {'view_name': 'api-country-detail'}
        }


class ChamberSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Chamber
        fields = ('id', 'url', 'name', 'abbreviation', 'country')
        extra_kwargs = {
            'url': {'view_name': 'api-chamber-detail'},
            'country': {'view_name': 'api-country-detail'}
        }


class EmailSerializer(serializers.HyperlinkedModelSerializer):

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


class ConstituencySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Constituency
        fields = ('id', 'url', 'name')
        extra_kwargs = {
            'url': {'view_name': 'api-constituency-detail'}
        }


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Group
        fields = ('id', 'url', 'name', 'abbreviation', 'kind')
        extra_kwargs = {
            'url': {'view_name': 'api-group-detail'}
        }


class MandateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Mandate
        fields = (
            'id',
            'url',
            'representative',
            'group',
            'constituency',
            'role',
            'begin_date',
            'end_date',
        )

        extra_kwargs = {
            'url': {'view_name': 'api-mandate-detail'},
            'group': {'view_name': 'api-group-detail'},
            'constituency': {'view_name': 'api-constituency-detail'},
            'representative': {'view_name': 'api-representative-detail'}
        }

    def to_internal_value(self, data):
        data = super(MandateSerializer, self).to_internal_value(data)
        data['group'] = models.Group.objects.get(
            id=data['group']['id']
        )
        data['constituency'] = models.Constituency.objects.get(
            id=data['constituency']['id']
        )
        data['representative'] = models.Representative.objects.get(
            id=data['representative']['id']
        )
        return data


class MandateDetailSerializer(MandateSerializer):
    group = GroupSerializer()
    constituency = ConstituencySerializer()

    class Meta(MandateSerializer.Meta):
        fields = (
            'id',
            'url',
            'group',
            'constituency',
            'role',
            'begin_date',
            'end_date',
        )


class RepresentativeSerializer(serializers.HyperlinkedModelSerializer):
    contacts = ContactField()

    mandates = MandateDetailSerializer(many=True)

    class Meta:
        model = models.Representative
        fields = (
            'id',
            'url',
            'slug',
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
            'mandates'
        )
        extra_kwargs = {
            'url': {'view_name': 'api-representative-detail'},
        }


class RepresentativeDetailSerializer(RepresentativeSerializer):
    pass
