from django.db import IntegrityError

from rest_framework import generics, status
from rest_framework.response import Response

from videos.models import Video
from videos.permissions import VideoViewPermissions
from videos.serializers import VideoSerializer, CreateVideoSerializer

from eswrapper.script import create_document


class ListVideos(generics.ListCreateAPIView):

    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (VideoViewPermissions, )

    def post(self, request, *args, **kwargs):
        serializer = CreateVideoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            v = Video.objects.create(**serializer.data)
            create_document(v)
            return Response(VideoSerializer(v).data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(status=status.HTTP_409_CONFLICT)


class VideoDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (VideoViewPermissions, )
    lookup_url_kwarg = 'video_pk'
