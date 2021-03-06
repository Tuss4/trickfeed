from django.conf.urls import patterns, url

import video_api
import tricker_api


urlpatterns = patterns('',
    # Videos
    url(r'^videos/?$', video_api.ListVideos.as_view(), name='list_videos',),
    url(r'^videos/es/?$', video_api.ESVideoList.as_view(), name='list_es_videos',),
    url(r'videos/(?P<video_pk>\d+)/?$', video_api.VideoDetail.as_view(), name='video_detail',),
    url(r'^tricker/register/?$', tricker_api.RegisterTrickerView.as_view(), name='register_tricker',),
)
