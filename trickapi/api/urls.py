from django.conf.urls import patterns, url

import video_api


urlpatterns = patterns('',
    # Videos
    url(r'^videos/?$', video_api.ListVideos.as_view(), name='list_videos',),
)
