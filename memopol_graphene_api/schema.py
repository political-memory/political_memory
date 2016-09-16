import graphene

from .schemas.representative import RepresentativeQuery


class Query(RepresentativeQuery):
    pass


schema = graphene.Schema(name='Memopol Schema')
schema.query = Query
