from representatives.management.remove_command import RemoveCommand

from representatives_votes.models import Dossier


class Command(RemoveCommand):
    manager = Dossier.objects
    conditions = {'proposals': None}
