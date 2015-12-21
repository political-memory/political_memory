from representatives.management.remove_command import RemoveCommand

from representatives.models import Representative


class Command(RemoveCommand):
    conditions = {'positions': None}
    manager = Representative.objects
