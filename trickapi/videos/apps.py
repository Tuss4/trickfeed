from django.apps import AppConfig


class VideosAppConfig(AppConfig):

    name = 'videos'
    verbose_name = 'videos'

    def ready(self):
         import videos.signals
