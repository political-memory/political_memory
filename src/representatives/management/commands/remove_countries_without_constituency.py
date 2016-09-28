from ..remove_command import RemoveCommand

from representatives.models import Country


class Command(RemoveCommand):
    manager = Country.objects
    conditions = {'constituencies': None}
