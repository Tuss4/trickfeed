from django.core.management.base import AppCommand
from eswrapper.mapping_script import create_index


class Command(AppCommand):

    help = "Index and document creation command."

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--new-index', dest='new_index',  default=False, type=bool,
            help='Flag to indicate that a new index is being created.')
        parser.add_argument(
            '--model', dest='model_name',
            help='Model name for index creation.')
        parser.add_argument(
            '--create-documents', dest='create_docs')

    def handle_app_config(self, app_config, **options):
        n_index = options.get('new_index')
        m_name = options.get('model_name')
        if n_index is True:
            if not m_name:
                self.stderr.write('No model name specified.')
            else:
                self.stdout.write('Creating index.')
                create_index(app_config, m_name)
                self.stdout.write('Done.')
