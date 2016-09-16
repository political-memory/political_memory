from graphene import relay, ObjectType
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene.contrib.django.types import DjangoNode

from representatives.models import Representative


class RepresentativeNode(DjangoNode):
    class Meta:
        model = Representative
        filter_fields = ['full_name']


class RepresentativeQuery(ObjectType):
    representative = relay.NodeField(RepresentativeNode)
    all_representatives = DjangoFilterConnectionField(RepresentativeNode)

    class Meta:
        abstract = True
