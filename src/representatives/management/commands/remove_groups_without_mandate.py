from ..remove_command import RemoveCommand

from representatives.models import Group


class Command(RemoveCommand):
    manager = Group.objects
    conditions = {'mandates': None}
