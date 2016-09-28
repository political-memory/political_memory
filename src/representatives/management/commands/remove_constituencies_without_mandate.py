from ..remove_command import RemoveCommand

from representatives.models import Constituency


class Command(RemoveCommand):
    manager = Constituency.objects
    conditions = {'mandates': None}
