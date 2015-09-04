from django.db import IntegrityError

from rest_framework import generics, status
from rest_framework.response import Response

from videos.models import Video
from videos.permissions import VideoViewPermissions
from videos.serializers import VideoSerializer, CreateVideoSerializer


class ListVideos(generics.ListCreateAPIView):

    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (VideoViewPermissions, )

    def post(self, request, *args, **kwargs):
        serializer = CreateVideoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            Video.objects.create(**serializer.data)
            return Response(status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(status=status.HTTP_409_CONFLICT)
