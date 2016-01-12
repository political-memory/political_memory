from representatives.management.remove_command import RemoveCommand

from representatives_votes.models import Proposal


class Command(RemoveCommand):
    conditions = {'recommendation': None}
    manager = Proposal.objects
