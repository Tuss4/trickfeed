from django.core.management.base import AppCommand
from eswrapper.script import delete_index, create_index, create_document
from eswrapper.exceptions import IndexNotFound

import time


WRNING_MSG = "Warning: This option will destroy your index and documents. Do you wish to continue? (y/n)"
DOC_CREATED_MSG = "Success creating document {}"


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
            m = app_config.get_model(m_name)
            # TODO: Add check to see if current mapping differs from mapping on node.
            self.stderr.write(WRNING_MSG)
            a = raw_input()
            if a == 'y':
                self.stdout.write("Destroying '{}' index.".format(m.get_index_name()))
                try:
                    delete_index(m.get_index_name())
                    self.stdout.write("Done.")
                    self.stdout.write("Re-creating index.")
                    create_index(app_config, m_name)
                    self.stdout.write("Done.")
                    self.stdout.write("Re-creating documents.")
                    time.sleep(3)  # To avoid overloading the node.
                    for obj in m.objects.all():
                        err = create_document(obj)
                        if not err:
                            self.stdout.write(DOC_CREATED_MSG.format(obj.pk))
                        else:
                            self.stderr.write(err)
                except IndexNotFound as e:
                    self.stderr.write(e.__str__())
            else:
                self.stdout.write("Operation cancelled.")
