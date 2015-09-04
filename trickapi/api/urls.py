from django.conf.urls import patterns, url

import video_api
import tricker_api


urlpatterns = patterns('',
    # Videos
    url(r'^videos/?$', video_api.ListVideos.as_view(), name='list_videos',),
    url(r'^tricker/register/?$', tricker_api.RegisterTrickerView.as_view(), name='register_tricker',),
)
