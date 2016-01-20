from django.db import IntegrityError

from rest_framework import generics, status, views
from rest_framework.response import Response

from videos.models import Video
from videos.permissions import VideoViewPermissions
from videos.serializers import VideoSerializer, CreateVideoSerializer

from eswrapper.mixins import ESPaginationMixin


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
            return Response(VideoSerializer(v).data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(status=status.HTTP_409_CONFLICT)


class VideoDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (VideoViewPermissions, )
    lookup_url_kwarg = 'video_pk'


class ESVideoList(ESPaginationMixin, views.APIView):

    def get(self, request, *args, **kwargs):
        qs = Video.es_objects.all()
        resp = self.esresp(Video.objects.count(), qs)
        return Response(resp, status=status.HTTP_200_OK)
