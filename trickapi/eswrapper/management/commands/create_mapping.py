from django.core.management.base import AppCommand


class Command(AppCommand):

    help = "A prototype command to generate an elasticsearch map for a django model"

    # def handle(self, *args, **options):
    #     self.stdout.write("Bruh")
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--model', default=None, dest='model_name',
            help="Specify a particular model from the app.")

    def handle_app_config(self, app_config, **options):
        print app_config.name
        print[m for m in app_config.get_models()]
        model_name = options.get('model_name')
        if model_name:
            print app_config.get_model(model_name)
