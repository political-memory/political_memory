from representatives.management.remove_command import RemoveCommand

from representatives.models import Representative


class Command(RemoveCommand):
    manager = Representative.objects
    conditions = {'votes': None}
