from eswrapper.mixins import ESManager
from django.apps import apps


class ESVideoManager(ESManager):

    def get_model(self):
        return apps.get_app_config('videos').get_model('Video')
