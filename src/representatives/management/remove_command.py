from django.core.management.base import BaseCommand


class RemoveCommand(BaseCommand):
    conditions = {}
    manager = None

    def add_arguments(self, parser):
        parser.add_argument('--dry',
            action='store_true',
            default=False,
            help='Do not actually execute delete')

    def handle(self, *args, **options):
        remove = self.manager.filter(**self.conditions)
        keep = self.manager.exclude(**self.conditions)

        print 'Delete %s %s, should remain %s' % (remove.count(),
            self.manager.model._meta.verbose_name_plural, keep.count())

        if options.get('dry', False):
            return

        remove.delete()
