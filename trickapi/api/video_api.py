from rest_framework import generics
from videos.models import Video
from videos.serializers import VideoSerializer
from rest_framework.permissions import AllowAny


class ListVideos(generics.ListAPIView):

    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (AllowAny, )
