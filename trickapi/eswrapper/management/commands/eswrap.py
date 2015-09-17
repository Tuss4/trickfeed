from django.core.management.base import AppCommand
from eswrapper.mapping_script import create_index, create_document


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
            '--create-documents', dest='create_docs', default=False, type=bool,
            help='Create documents for every instance in the specified model.')

    def handle_app_config(self, app_config, **options):
        n_index = options.get('new_index')
        c_docs = options.get('create_docs')
        m_name = options.get('model_name')
        if not m_name:
            self.stderr.write('No model name specified.')
        else:
            if n_index:
                self.stdout.write('Creating index.')
                create_index(app_config, m_name)
                self.stdout.write('Done.')
            if c_docs:
                model = app_config.get_model(m_name)
                for m in model.objects.all():
                    err = create_document(m)
                    if not err:
                        self.stdout.write('Success creating document {}.'.format(
                            m.pk))
                    else:
                        self.stderr.write(err)
