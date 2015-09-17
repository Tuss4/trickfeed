from django.core.management.base import AppCommand


WRNING_MSG = "Warning: This option will destroy your index and documents. Do you wish to continue? (y/n)"


class Command(AppCommand):

    help = "Update mapping or settings on index. Will re-create index and re-create documents."

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--model', dest='model_name',
            help='Specify the model.')

    def handle_app_config(self, app_config, **options):
        m_name = options.get('model_name')
        if not m_name:
            self.stderr.write("Model name missing.")
        else:
            # TODO: Add check to see if current mapping differs from mapping on node.
            self.stderr.write(WRNING_MSG)
            a = raw_input()
            if a == 'y':
                self.stdout.write("Doing thangs.")
            else:
                self.stdout.write("Operation cancelled.")
