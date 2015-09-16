from django.core.management.base import AppCommand
from eswrapper.mapping_script import create_mapping


class Command(AppCommand):

    help = "A prototype command to generate an elasticsearch map for a django model"

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--model', default=None, dest='model_name',
            help="Specify a particular model from the app.")

    def handle_app_config(self, app_config, **options):
        model_name = options.get('model_name')
        if model_name:
            self.stdout.write(
                "Creating mapping for {0} in '{1}/es_mappings.py'".format(
                    model_name, app_config.path))
            try:
                create_mapping(app_config, model_name)
                self.stdout.write("Done.")
            except LookupError:
                self.stderr.write(
                    "App '{0}' does not have a '{1}' model.".format(
                        app_config.name, model_name))
